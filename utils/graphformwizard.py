"""
Advanced FormWizard class -- supports constrained graph-based scenario's.

Uses GraphFormWizardSession model to store intermediate data. Stores temporary
files in special directory in order to preserve them between wizard steps.

To create a new wizard you should extend GraphFormWizard in order to:
  - define the scenario
  - define final done() method, that handles the collected and successfully validated data.

If branching is used, the branching logic should be implemented. You may define
callable guards directly in the scenario or extend guard_step() method that
will handle all other branches.

Just like django.contrib.formtools.wizard.FormWizard you can use GraphFormWizard
sub-classes directly in your urls.py.


== Edit data ==
In most cases to create and edit object you will use different wizards, since
editing is usually a simpler process. For example, to create a new book you can
define:
  - "create" wizard that collects info about the book and cycles over all authors.
    When book is saved, you will create book and add authors at once.
  
  - "edit book" wizard, that allows the users to edit info. about the book
  - "add authors" wizard, allows the user to define new or edit existing authors
    of the book.

In the example above only the "create" wizard is complex enough to contain a cycle.
All other wizards are simple one line sequence of steps, that may however be
iterating (cycled) from initial up to the final step explicitly. Of course you
may use "create" wizard to edit everything, but this approach may suffer from
usability issues.

To edit the data you will have to define a view that will:
  - load all models and the data needed by the scenario
  - re-create dict/list structures ad described by done() method
  - call YourWizardSubclass.save_data(data) -- this will save the data in the session
  - redirect to the wizard's initial or any other step

The drawback is that your data needs to be decoupled from the model instances
you use and stored separatedly as dict objects. Another problem is that wizard
returns validated data along the path user has taken in the scenario. If complex
branching is used, then it is the responsibility of the subclass to determine
how data was changed and how the changes should be handled.


== Scenario ==
A wizard is nothing more than a graph of pages (templates) with corresponding
sets of forms for each page. The steps are arranged in a constrained graph. Most
simple graph is a sequence [step1..stepN]. More complicated graphs contain:
 - cyles -- the user can repeat a subpath
 - branches and merges -- depending on some logic wizard takes one of the branches

The branches allow switching the wizard behavior based on prior choices made by
the user. There is no restriction on complexity of the the branching/merging,
but always keep in mind the usability. The wizard can tell the user how many
steps are there up to the next branch, the user may loose the sense of size of
the wizard (boring long wizards are nasty) if there are to many branches.

The cycle allows the user to step back and repeat the sub-path. The GUI controls
will be shown to the user to control the cycle. The user can switch to one of
the sub-paths in the cycle, cancel a cycle etc.

There are limitations in the wizard's logic:
 - merge is not a go-to, graph implicit cyclicity check is used to prevent inproper use
 - sub-paths in different cycles can not be merged together
 - nested cycles are strictly distinct, same limitations as to neigboring cycles.
 - all outgoing branches from a cycle should meet in the same step of outer cycle/context


== Actions and GET/AJAX handlers ==
Each wizard's page is assumed to be POST'ed in order to proceed to the next page.
Sometimes you want to introduce simple GET links to:
  - perform AJAX calls specific to a step
  - perform some general logic (repeat/cancel cycle, enable something, help etc)

The wizard recognizes actions as simple names appended to wizard's URL. Some of
the actions are reserverd (eg. post, cancel). All others will be redirected to
wizard_action() method that can be overriden by the subclass. By default
wizard_action() raises 404 error.

The wizard expects current path in the scenario specified in the URL. This allows
you to build persistent URL's to steps (providing you have valid data in your session).
The wizard will always try to reconstruct-revalidate the whole path, on mismatch
the user will be redirected to the last valid step. The path is a sequence of
[a-z] letters representing branches, it will be compressed by RLE. So, if your
scenario is a sequence [step1..step6], then your step5 will have the URL path "a5",
which will be internally expanded to "AAAAA". The path may contain more information,
like the selection of the concrete cycle.

If you are on the step "/a3b:2a" and you want to perform AJAX call, then your URL
will become "/a3b:2a/my_action". By GET'ing this URL the wizard will redirect the
call to wizard_action('my_action', ...), there from you can build your step
specific response.


== URL's ==
This wizard may be used as a view. The URL patterns are expected to be:
  - 'wizard.step' - "/(?P<path>[a-z0-9:]*)$"
    Navigate to the step. If POST request is made, then step will be validated
    and wizard will proceed to the next step (redirects to next step URL).
  
  - 'wizard.action' - "/(?P<path>[a-z0-9:]*)/(?P<action>[a-zA-Z][a-zA-Z0-9_]*)$"
    The same as the URL above, but specifies action label (used for GET/AJAX queries).
  
  - you may specify more urls containing "action" pattern. If action is provided,
    then wizard will redirect all *args, **kwargs to wizard_action(). So you
    can specify URL patterns with arguments for your actions. Example:
    "/(?P<path>[a-z0-9:]*)/(?P<action>calendar)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$"


In general, if POST request is sent, then result should be a redirect to reflect
path change in URL.


== Config ==

WIZARD_TIMEOUT -- datetime.timedelta to substract from datetime.now(). If the
 user has lost it's session while being in the middle of the wizard scenario,
 then we can still recover by fetching the last uncompleted session. If this
 option is set, then such uncompleted session may not be older than given timedelta.

WIZARD_KEEP_DATA -- if True, then wizard will not delete session object, but mark
 them complete. I don't know why we need this garbage, but this feature was required.

WIZARD_UPLOAD_TEMP_DIR -- path to directory where uploaded files should be moved.
 The wizard will not delete temporary files (should be persistent in a session),
 so a cronjob is needed to remove old files. If not set, then standard TMP directory
 will be used.


Author: Sardar Yumatov (ja.doma@gmail.com)

"""

import re
import cPickle
import datetime
import tempfile
import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.forms import Form
from django.core.files.uploadedfile import UploadedFile

# used to store session data
from utils.models import GraphFormWizardSession



class Step(object):
    """
        Single wizard step.
        
        This class allows you to build chained definition of the whole scenario.
        Nothing will be checked since the scenario is usually build when class
        is loaded (scenario is a static variable). The whole resolution and
        consistency checks will be executed when instance is created (usually
        within urls.py)
    """
    
    
    def __init__(self, name, template = None, extra_context = None, **kwargs):
        """
            Create new empty step.
            
            @param name unique name of the step
            @param template step specific template
            @param extra_context extra data, will be available in template
            @param kwargs additional arguments that will be available as fields (eg. title etc)
        """
        self.template = template
        self.extra_context = extra_context
        self.name = name
        self.forms = {}
        self.fields = kwargs
        
        #invariant: not more than one of (next, merge, branches) is not empty
        # yes, only branche() is enough, but we want make constrained declarations
        # to minimize errors. Step.next() -- means there is only one branch - next.
        # Step.branch() means there could be more than one branch. This simple
        # check prevents hidden bugs in scenario's.
        self._next = None
        self._merge = None
        self._branches = []
        self.initial = self  # used to find initial step in branches
        # marks the cycle
        self._cycle_start = False
        self._cycle_template = None
        self._cycle_extra_context = None
        self._cycle_end = False

    
    def form(self, name, cls, prefix = None, initial = None):
        """
            Add form to the step.
            
            There can be as many forms as you like. How the forms will be
            rendered is up to the template. Default template will render the
            forms in order they were added.
            
            Initial value is the static value used by all wizard in "new/create"
            mode. Different kinds of forms require different initial value.
            Normal form uses initial(dictionary), management_form expects the
            query set as initial parameter and model form requires model instance.
            
            Warning: if initial value is given for the model form, then you will
            always edit that model instance when calling form.save(), this is
            probably not what you want to do.
            
            Note: prefix is used by the form to distinguish its data in request.POST
            If you have multiple instances of the same form class, then unique
            prefix is mandatory.
            
            @param name unique within the step name of the form
            @param cls the form class
            @param prefix the form prefix, step name will be appended to it
            @param initial initial static object/value (not for editing mode)
            @return self
        """
        prefix = u'%s_%s_%s' % (self.name, name, prefix) if prefix is not None else  u'%s_%s' % (self.name, name)
        
        if name in self.forms:
            raise ImproperlyConfigured("%s: form or data named '%s' is already defined" % (self.name, name))
        
        self.forms[name] = (cls, prefix, initial)
        return self

    
    def data(self, **kwargs):
        """
            Add static data. This data will be available as step.field's
            
            Example:
                .data(title = "my title")
            
            Note: you can also specify fields in the constructor.
            
            @return self
        """
        self.fields.update(kwargs)
        return self

    
    def next(self, name, template = None, extra_context = None, **kwargs):
        """
            Create and attach new step.
            
            @param name unique name of the new step
            @param template specific template for the new step
            @param extra_context extra data, will be available in template
            @param kwargs additional arguments that will be available as fields (eg. title etc)
            @return Step new step
        """
        
        # impossible if only chained operations are used (no variables)
        if self._next is not None:
            raise ImproperlyConfigured("%s: next step is already defined: '%s', rejecting new '%s', use branch for multiple next branches" % (self.name, self._next.name, name))
        
        # later we will check if name is unique
        nstep = Step(name, template, extra_context, **kwargs)
        nstep.initial = self.initial
        self._next = nstep
        return nstep

    
    def branch(self, step, guard = None):
        """
            Creates guarded branch.
            
            The guarded branch is the sub-path, that can be entered if and only
            if the guard evaluates to true. If guard is None, then default
            (overriden by the wizard's subclass) guard will be used.
            
            If guard == True, then default branch will be created (equivalent to
            next() call). There can be only one default (unguarded) branch. The
            default branch will be used if all other branches are rejected.
            
            The @step can be given as Step object or as a string reference (name).
            If the step is given by name, then the branch acts as guarded merge.
            Equivalent reachability checks will be performed.
            
            Note: branch lookups to the first step created by directly invoking
            the constructor. This allows you to write .branch(Step('first').next().next())
            and the branch will be linked to the 'first' step.
            
            @param step the next step as Step object or name
            @param guard optional guard, either callable or True
            @return self
        """
        if not callable(guard) and guard is not True and guard is not None:
            raise ImproperlyConfigured("%s: the guard should be callable, True or None" % self.name)
        
        # branch accpets new Step, which may be chained further. to access the
        # first step we use dirty hack: step.initial
        self._branches.append((step.initial if isinstance(step, Step) else step, guard))
        return self

    
    def merge(self, stepname):
        """
            Merge current branch with an another.
            
            The merge operation can be seen as next() call with already existing
            step. Current step must not be reachable from the target step to
            prevent implicit cycles.
            
            Merge will close current sub-path. In order to merge as part of a
            branch use branch() with step given by name.
            
            Note: the merge call should be seen as if it returns None, because
            this is the last call on the branch. To let the branches work
            correctly this method returns self, but it is not intended for
            further chained calls.
            
            @param stepname name of the step
            @return self by design returns None (because of technical reasons, returns self)
        """
        # impossible if only chained operations are used (no variables)
        if self._merge is not None:
            raise ImproperlyConfigured("%s: merge is already defined: '%s', rejecting new '%s', use branch for multiple merges" % (self.name, self._merge, stepname))
        
        if isinstance(stepname, Step):
            raise ImproperlyConfigured("%s: you should merge to the step by name (you merge to existing path). If you have the step object (%s), then you should continue with your branch with branch() call" % (self.name, stepname.name))
        
        self._merge = stepname
        return self

    
    def cycle(self, template = None, extra_context = None):
        """
            Mark this step as a start of the cycle.
            
            This and all subsequent steps until end() will be within this cycle.
            This step is called 'head' of the cycle. There can be only one head
            and the step can be only in one cycle.
            
            @param template default template for all steps within this cycle
            @param extra_context extra content to pass to template within this cycle
            @return self
        """
        
        # defined here in order to not loose double start_cycle() call, harder to find bug
        if self._cycle_start:
            raise ImproperlyConfigured("%s: cycle is already started, you can not start multiple cycles from the same step" % self.name)
        
        self._cycle_start = True
        self._cycle_template = template
        self._cycle_extra_context = extra_context
        return self

    
    def end(self):
        """
            Mark this step as end of the cycle.
            
            This step willbe part of the current cycle, but all subsequent steps
            will be part of the outer cycle. This step is called 'tail'. There
            can be multiple tails of the cycle.
            
            @return self
        """
        
        # defined here in order to not loose double end_cycle() call, harder to find bug
        if self._cycle_end:
            raise ImproperlyConfigured("%s: cycle is already closed, you can not close multiple cycles from the same step" % self.name)
        
        self._cycle_end = True
        return self



class CleanStep(object):
    """Cleaned step. Properly validated scenario step."""
    
    def __init__(self, step, ctx, cycle):
        self.name = step.name
        self.forms = step.forms
        self.template = step.template
        self.extra_context = step.extra_context
        self._fields = step.fields
        self.next = None
        self.default = None
        self._head = False
        self._tail = False
        self._mark = True
        
        # names are unique
        if self.name in ctx:
            raise ImproperlyConfigured("%s: name '%s' is not unique" % (step.name, step.name))
        ctx[self.name] = self
        
        # start cycle (head)
        # there can be only one head
        if step._cycle_start:
            cycle = cycle.nest(self, step._cycle_template, step._cycle_extra_context)
            self._head = True
        
        self.cycle = cycle
        self.cycle.add(self)
        
        # end cycle (tail)
        # there can be multiple tails
        if step._cycle_end:
            cycle = cycle.back(self)
            self._tail = True
        
        # prevents hard to find bugs in declarations
        ct = 0
        if step._next is not None: ct += 1
        if step._merge is not None: ct += 1
        if len(step._branches) > 0: ct += 1
        if ct > 1:
            raise ImproperlyConfigured("%s: mixed next/merge/branche calls" % self.name)
        
        # leaf (wizard end point), top level cycle
        if not step._cycle_end and ct == 0:
            # last step is required, not technically, but just for usability
            if self.cycle.level > 0:
                raise ImproperlyConfigured("%s: last step is in cycle of level %d, for usability close the cycle in this step and next() to the final step (create final step if needed)" % (self.name, self.cycle.level))
            self.cycle.back(self)
        
        # leaf, there can be many of them
        if ct == 0:
            return
        
        # simple next step case
        if step._next is not None:
            if isinstance(step._next, Step):
                self.next = CleanStep(step._next, ctx, cycle)
            else:
                self.next = step._next   # will be resolved later
        elif step._merge is not None:    # merge case, will be resolved later
            self.next = step._merge
        else:                           # multiple branches case
            self.next = {}
            for i, (ch, gr) in enumerate(step._branches):
                if isinstance(ch, Step):
                    ch = CleanStep(ch, ctx, cycle)
                
                if gr is True:
                    if self.default is not None:
                        raise ImproperlyConfigured("%s: only one default branch is allowed" % self.name)
                    
                    self.default = ch
                
                else:
                    key = GraphFormWizard.branch_code[i]
                    self.next[key] = (ch, gr) # will be resolved later
            # end for

    
    def resolve(self):
        """Resolve all name references within the cycle."""
        # prevents endless recursion (we don't check cyclicity yet)
        if not self._mark:
            return
        
        self._mark = False
        if isinstance(self.next, dict):     # if multiple branches
            for (key, (ch, gr)) in self.next.items():
                if not isinstance(ch, CleanStep):
                    chstep = (self.cycle.get(ch), gr)
                    if ch is None:
                        raise ImproperlyConfigured("%s: branch-merge with '%s', step is not found" % (self.name, ch))
                    
                    self.next[key] = chstep
                else:
                    ch.resolve()
            
            if self.default is not None:
                if not isinstance(self.default, CleanStep):
                    self.default = self.cycle.get(self.default)
                else:
                    self.default.resolve()

        
        elif self.next is not None:
            if not isinstance(self.next, CleanStep):
                nnx = self.cycle.get(self.next)
                if nnx is None:
                    raise ImproperlyConfigured("%s: merge with '%s', step is not found" % (self.name, self.next))
                
                self.next = nnx
            else:
                self.next.resolve()

    
    def check_cycle(self):
        """Checks implicit cycles."""
        # brute force O(N^2) check, no time to implement something more efficient
        if self._mark:
            raise ImproperlyConfigured("%s: implicit cycle detected, this step is reached twice!" % self.name)
        
        self._mark = True
        if isinstance(self.next, dict):     # if multiple branches
            for (key, (ch, gr)) in self.next.items():
                ch.check_cycle()
        
        elif self.next is not None:
            self.next.check_cycle()
        
        self._mark = False

    
    def is_final(self):
        """True if this step is final (no next)"""
        return self.next is None
    
    def is_head(self):
        """True if this is the head of the cycle"""
        return self._head
    
    def is_tail(self):
        """True if this is the one of the tails of the cycle"""
        return self._tail

    
    def get_straight_branch(self):
        """
            Returns None if this steps contains multiple branches (or guarded)
            or is final
        """
        if self.next is not None:
            if isinstance(self.next, dict):
                if len(self.next) == 0 and self.default is not None:
                    return self.default
            
            else:
                return self.next
        
        return None

    
    def get_branch(self, letter):
        """Returns branch encoded by letter"""
        if self.next is not None:
            if isinstance(self.next, dict):
                if self.default is not None and GraphFormWizard.branch_code[len(self.next)] == letter:
                    return self.default
                
                return self.next.get(letter, None)[0]
            
            elif letter == 'A':
                return self.next
        
        return None
    
    def encode_branch(self, step):
        """Returns encoding letter for given CleanStep"""
        if not isinstance(self.next, dict):
            return 'A' if step is self.next else None
        
        else:
            cand = [l for (l, (s, _)) in self.next.iteritems() if s is step]
            if len(cand) < 1 and step is self.default:
                cand.append(GraphFormWizard.branch_code[len(self.next)])
            
            assert len(cand) <= 1
            if len(cand) > 0:
                return cand[0]
        
        return None

    
    def get_forms(self, stepdata, post = None, files = None):
        """Re-instantiates forms"""
        #(valid, stepforms, cleandata)
        retforms = {}
        retdata = {}
        valid = True
        for (name, (form, prefix, initial)) in self.forms.iteritems():
            # model form
            if hasattr(form, 'Meta') and hasattr(form.Meta, 'model'):
                init = 'instance'
            # management form
            elif hasattr(form, 'management_form'):
                init = 'queryset'
            # normal form (initialized from dictionary)
            else:
                init = 'initial'
            
            kwargs = {
                init: initial,
                'prefix' : prefix
            }
            
            args = stepdata.get(name, ({}, {}))
            if post is not None:
                args[0].update(post)
            
            if files is not None:
                args[1].update(files)
            
            retforms[name] = form(*args, **kwargs)
            valid = valid and retforms[name].is_valid()
            retdata[name] = getattr(retforms[name], 'cleaned_data', {})
        
        return (valid, retforms, retdata)

    
    def __getattribute__(self, name):
        """Access to additional fiels (eg. title)"""
        # this will be used in templates, forget about AttributeError's
        try:
            return object.__getattribute__(self, name)
        except:
            fl = object.__getattribute__(self, '_fields')
            return fl.get(name, None)
    
    def __repr__(self):
        return self.name


class CycleContext(object):
    """Holds the steps of the single cyle"""
    
    def __init__(self, level = 0, parent = None, template = None, extra_context = None):
        self.level = level          # current level starting from 0
        self.parent = parent        # parent cycle
        self.subcycles = []         # all sub-cycles
        self.head = None            # head step of the cycle
        self.template = template    # template for all steps within this cycle
        self.extra_context = extra_context  # extra template data
        self.tails = {}             # all tail steps in this cycle
        self.outer_tail = None      # where all tail steps meed or None if all tails are final
        self.steps = {}             # all steps in this cycle by name
        self.is_final = False       # will be true if all tails are final
    
    def nest(self, head, template = None, extra_context = None):
        ccl = CycleContext(self.level + 1, self, template, extra_context)
        ccl.head = head
        self.subcycles.append(ccl)
        return ccl
    
    def back(self, tail):
        self.tails[tail.name] = tail
        return self.parent
    
    def add(self, step):
        self.steps[step.name] = step
    
    def get(self, name):
        return self.steps.get(name, None)
    
    def check_merge(self):
        """Ensure all tails meet in the same step or all are final steps"""
        if len(self.tails) < 1:
            raise ImproperlyConfigured("Cycle without tails? Wizard should not allow this, a bug in wizard base detected!")
        
        out = {}
        fin = False
        allfin = True
        for stp in self.tails.itervalues():
            if stp.is_final():
                fin = True
            
            else:
                allfin = False
                if isinstance(stp.next, dict):
                    for (st, gr) in stp.next.itervalues():
                        out[st.name] = st
                
                else:
                    out[stp.next.name] = stp.next
        
        #end for
        
        # this cycle is either final (all steps are final) or meet in one outer step
        if fin and not allfin:
            raise ImproperlyConfigured("You can not mix final and non final steps in one cycle")
        
        elif not allfin and len(out) != 1:
            raise ImproperlyConfigured("All tail steps in a cycle should meet in one step of the outer cycle")
        
        outer_tail = out.itervalues().next() if len(out) > 0 else None
        
        if outer_tail is not None and outer_tail.cycle is self: # this can not happen or previous checks are buggy
            raise ImproperlyConfigured("Implicit cycling detected! Wizard has not detected it before, bug in wizard detected!")
        
        self.is_final = fin
        self.outer_tail = outer_tail
        
        for sub in self.subcycles:
            sub.check_merge()



class SessionUploadedFile(UploadedFile):
    """
        A file uploaded to a temporary location, which is persistent, so this
        instance can be saved in session.
    """
    def __init__(self, path, file, content_type, size, charset):
        # name, content_type, size, charset
        self.moved_path = path
        self.failed = False
        try:
            super(SessionUploadedFile, self).__init__(file, path, content_type, size, charset)
        except:
            self.failed = True
    
    def temporary_file_path(self):
        """ Returns the full path of this file. """
        return self.moved_path
    
    def __getstate__(self):
        """Pickle support, store links"""
        if self.failed:  # should not happen. If file is failed, then it should be removed
            return False
        
        try: # close handler
            self.close()
        except:
            pass
        
        return {
            'path': self.moved_path,
            'content_type': self.content_type,
            'size': self.size,
            'charset': self.charset
        }
    
    def __setstate__(self, dat):
        """Pickle support, restore state"""
        if dat is not False:  # check if file still exists
            try:
                file = open(dat['path'], "rb+")
                # become alive
                self.__init__(dat['path'], file, dat['content_type'], dat['size'], dat['charset'])
                return
            except:
                pass
        
        self.failed = True


class GraphFormWizard(object):
    """Advanced form wizard."""
    
    # subclasses should re-define static scenario
    scenario = None
    
    # If some of your actions are lightweight, then specify them here
    # read more in wizard_fast_action()
    # eg. frozenset(['my_action', 'my_other_action'])
    fast_actions = frozenset([])
    
    # encoding used for branches, single letter
    branch_code = ''.join([chr(i) for i in xrange(ord('A'), ord('Z')+1)])
    co_path_reg = re.compile('((?:(?P<prev>[A-Z])(?P=prev)*)|(?:\:[0-9]+))')
    de_path_reg = re.compile('(([A-Z])([0-9]*)|(?:\:[0-9]+))')
    path_reg = re.compile('(?:([A-Z])(?:\:([0-9]+))?)|(?:\:([0-9]+))')
    
    # default actions implemented by this wizard
    built_in_actions = frozenset(['post', 'cancel', 'reset'])

    
    def __init__(self, name = None, template = None):
        """ Construct new wizard. Usually invoked from urls.py
            
            @param name wizard's name, required when multiple wizard instances are allowed in the session
            @param template default template for all steps
        """
        self.template = template
        self.name = name
        
        if self.scenario is None:
            raise ImproperlyConfigured("%s: subclass must define scenario" % self.name)
        
        self.steps = {}                     # all steps by unique name
        self.root_cycle = CycleContext()    # root cycle, knows first and last steps
        # raises exceptions on any inconsistency
        self.clean_scenario = CleanStep(self.scenario.initial, self.steps, self.root_cycle)
        self.clean_scenario.resolve()
        self.clean_scenario.check_cycle()
        self.root_cycle.check_merge()
        
        # OK, at this point we have consistent cool scenario

    
    # Called by the url dispatcher
    def __call__(self, request, path = '', action = None,
                        extra_context = None,
                        url_step = ('wizard.step', (), {}),
                        url_action = ('wizard.action', (), {}),
                        *args, **kwargs):
        """
            Handles requests (wizard is a view).
            
            @param request used for POST, FILES, session, user
            @param path current path in the wizard
            @param action if action call is being made (GET actions)
            @param extra_context will be available in template as-is
            @param url_step (name, args, kwargs) used to resolve URL's to steps
            @param url_action (name, args, kwargs) used to resolve URL's to actions
            @return HttpResponse
        """
        
        # current path in scenario
        (step_path, valid) = self.parse_path(self.uncompress_path(path))
        if not valid: # did scenario change? werid, redirect to the first step
            url = self.build_path(step_path)
            return HttpResponseRedirect(reverse(url_step[0], args = url_step[1], kwargs=dict(url_step[2], path = self.compress_path(url))))
        
        
        curstep = step_path[-1][0]
        # handle light weigth actions
        if action is not None and action not in self.built_in_actions and action in self.fast_actions:
            return self.wizard_fast_action(request, action, curstep, step_path, *args, **kwargs)
        
        # restore data
        (data, meta) = self.restore_data(request, *args, **kwargs)
        
        # handle files, move, replace links
        files = self.handle_files(request, *args, **kwargs)
        
        # cancel cycle, on steps has the same meaning as reset
        if action == 'cancel' or action == 'reset':
            if action == 'cancel': # delete cycle, reset step
                uppath = self.cancel_path(step_path, data)
            else:
                uppath = self.reset_path(step_path, data)
            
            self.save_data(request, data, meta, *args, **kwargs)
            url = self.compress_path(self.build_path(uppath))
            return HttpResponseRedirect(reverse(url_step[0], args = url_step[1], kwargs=dict(url_step[2], path = url)))
        
        # OK, now we need re-validated data along the path
        (valid, last_valid, wizard_data, step_context, validpath, lastforms) = self.refetch_path(step_path, data, request.POST, files)
        if not valid: # validpath is prefix of step_path
            return self.revalidation_failed_response(request, validpath, step_path, url_step = url_step, url_action = url_action, *args, **kwargs)
        
        # if some action should be invoked instead of default (fill -> next)
        if action is not None and action not in self.built_in_actions:
            ret = self.wizard_action(request, action, meta, curstep, step_context, step_path, wizard_data, data, *args, **kwargs)
            self.save_data(request, data, meta, *args, **kwargs)
            return ret
        
        
        # OK, perform default action
        if last_valid and (request.method == 'POST' or action == 'post'):
            # if we are done
            if curstep.is_final():
                self.clear_data(request, *args, **kwargs)
                return self.done(request, wizard_data, meta, *args, **kwargs)
            
            # proceed to the next step
            else:
                if isinstance(curstep.next, dict):
                    # multiple branches
                    nextstep = None
                    for (key, (step, guard)) in curstep.next.items():
                        if guard is None:
                            guard = self.guard_step
                        
                        # evaluate guard
                        if guard(request, step, step_context, step_path, wizard_data):
                            nextstep = step
                            break
                    # end for
                    
                    # nothing matched, try default step
                    if nextstep is None:
                        if curstep.default is None:
                            raise ImproperlyConfigured("No default branch is defined, all guards are evaluated to False. I'm stuck here!")
                        
                        nextstep = curstep.default
                else:
                    nextstep = curstep.next
                
                # we have next step, now branch
                step_path.append((nextstep, 0))
                url = self.build_path(step_path)
                self.save_data(request, data, meta, *args, **kwargs)
                return HttpResponseRedirect(reverse(url_step[0], args = url_step[1], kwargs=dict(url_step[2], path = self.compress_path(url))))
        
        # current step doesn't accept the data or it is not a POST/post request
        # we are going to render the page. fetch steps up to next visible branch
        tpldata = self.fetch_template_data(step_path, wizard_data, data, url_step, url_action)
        tplcurstep = {
            'step': curstep,
            'valid': last_valid,
            'forms': lastforms
        }
        
        template = curstep.template or curstep.cycle.template or self.template
        context = {
            'forms': lastforms,
            'steps': tpldata,           # complete steps info as returned by fetch_template_data()
            'curstep' : tplcurstep,     # part of steps, for current step only
            'meta_data': meta,          # current meta
            'step_path' : step_path,    # [ (CleanStep, int) ]
            'wizard_step_url': url_step,     # (url_name, args, kwargs)
            'wizard_action_url': url_action, # (url_name, args, kwargs)
            'step_url_path': self.build_path(step_path),  # current step path, to specify in wizard_step_url
            'current_step_is_valid': last_valid,    # if current is valid
            'step_context': step_context,           # allows you to lookup in previous steps
            'wizard_data': wizard_data              # allows you to lookup in all previous steps
        }
        
        if extra_context is not None:
            context.update(extra_context)
        
        if curstep.cycle.extra_context is not None:
            context.update(curstep.cycle.extra_context)
        
        if curstep.extra_context is not None:
            context.update(curstep.extra_context)

         
         # at this step we have: meta, curstep, step_context, step_path, wizard_data, data
        #print context
        #self.save_data(request, data, meta, *args, **kwargs)
        
        #from django.http import HttpResponse
        #return HttpResponse("""
#<html>
#<head></head>
#<body>
#<h1>Files</h1>
#
#<form action="" method="POST" enctype="multipart/form-data">
#    <input type="file" name="test_file">
#    <input type="submit" value="Send">
#</form>
#
#</body>
#</html>
#        """)
        
        return render_to_response(template, context, context_instance = RequestContext(request))


# data structure for templates
# (CleanStep, {forms}, {step_url: goto, reset}, is_current, is_on_path) -- single step in the path
# [ (), (), {}, (), None] -- path of the scenario to the end or to the branch:
#   () -- single step in scenario order
#   {} -- cycle (cycle head)
#   None -- indicates that last step is not final, we stopped at the branch
# {
#   'current': 0  -- current cycle index
#   'head': CleanStep -- cycle head
#   'current_path': (url, [ () ... ]) -- path at current index. url is cycle URL
#   'cycles': [ (url, valid, [ () ...]), (), ...] -- the cycles with corresponding URL's
# }
# URL can be directly used to navigate (for cycle we navigate to the head) or
# to cancel things (cancel cycle -- deletes it, cancel step - reloads it)
#
# Current step (CleanStep, filled forms) are defined in template. Compare with
# current_step to highlight current step.
#
# Note: URL's of the unreachable path's (not filled/validated) will be None, you
# can not bypass validation anyway.
    
    def fetch_template_data(self, step_path, wizard_data, data, url_step, url_action):
        """Re-arranges steps in the structure usable for templates"""
        # tplpath: [ ("step", step_info), (menu, menu_list), ..., ("branch", branch_info) ]
        #
        # ("step", step_info)
        # step_info: (is_on_path, is_current, is_valid, urls, CleanStep)
        #
        # ("branch", branch_info)
        # branch_info: {step_name: (CleanStep, goto_url)}
        #
        # ("menu", menu_list)
        # menu_list: ([ (is_complete, is_current, urls, [ (step, step), , (branch, ) ]) ])
        #
        # Urls:
        #  goto: go to step, None if step is invalid (except for current step, which may be invalid)
        #  reset: reset step (delete session data)
        #  cancel_cycle: only for head and tail steps, cancel this cycle
        #  new_cycle: only for tail steps, start from head with new cycle
        
        # it kills me... =(
        if len(step_path) < 1:
            step_path.append((self.clean_scenario, 0))
        
        curdata = data
        curdatastack = []
        curwiz = wizard_data
        curwizstack = []
        
        tplpath = []
        tgt = step_path[-1][0]
        urlpath = []
        urlheads = []
        
        # along the path, build menu data
        for (step, cycle) in step_path:
            urls = {}       # URL links
            urlpath.append((step, cycle))   # used to build path to prev steps
            
            if step.is_head(): # emit menu
                # we have to refetch cycles again because we don't know what whas filtered
                # in wizard_data =\
                cycles = curdata[step.name]    # everything is re-created by refetch_path()
                cycldat = [ self._fetch_template_cycle(idx, step, pt, cyctx) for (idx, (pt, cyctx)) in enumerate(cycles) ]
                tplpath.append(("menu", cycldat))   # add menu handle before head
                
                # we will go up the cycle, we need to restore context
                curdatastack.append(curdata)
                curwizstack.append(curwiz)
                curdata = cycles[cycle][1]      # go deeper in context
                curwiz = curwiz[step.name][-1]  # current is always the last
                
                cancel_cycle_url = reverse(url_action[0], args = url_action[1], kwargs=dict(url_action[2], action = 'cancel', path = self.compress_path(self.build_path(urlpath))))
                new_cycle_url = urlpath[0:-1]
                new_cycle_url.append((step, len(cycles)))
                new_cycle_url = reverse(url_step[0], args = url_step[1], kwargs=dict(url_step[2], path = self.compress_path(self.build_path(new_cycle_url))))
                urlheads.append((new_cycle_url, cancel_cycle_url))
                urls['cancel_cycle'] = cancel_cycle_url
            # end is head
            
            if step.is_tail(): # add controls to the step
                (newurl, cancurl) = urlheads.pop()
                urls['new_cycle'] = newurl
                urls['cancel_cycle'] = cancurl
            
            urls['goto'] = reverse(url_step[0], args = url_step[1], kwargs=dict(url_step[2], path = self.compress_path(self.build_path(urlpath))))
            urls['reset'] = reverse(url_action[0], args = url_action[1], kwargs=dict(url_action[2], action = "reset", path = self.compress_path(self.build_path(urlpath))))
            
            curdat = curwiz.get(step.name, None)
            tplpath.append(("step", {
                'is_on_path': True,
                'is_current': step is tgt,
                'is_valid': curdat is not None,
                'urls': urls,
                'step': step}))
            
            if step.is_tail(): # restore context
                curdata = curdatastack.pop()
                curwiz = curwizstack.pop()
        
        #end for
        
        # fetch steps beyond current path up to the final or undecided branch
        # step is the last step on step_path, curdata - current context
        # curdatastack - stacked context
        nextstep = step.get_straight_branch()
        while nextstep is not None:
            urls = {}       # URL links
            urlpath.append((nextstep, 0))   # used to build path to prev steps
            
            if nextstep.is_head():
                cycles = curdata.get(nextstep.name, [])
                curdatastack.append(curdata)
                curdata = cycles[0][1] if len(cycles) > 0 else {}
            # end is head
            
            urls['goto'] = reverse(url_step[0], args = url_step[1], kwargs=dict(url_step[2], path = self.compress_path(self.build_path(urlpath))))
            urls['reset'] = reverse(url_action[0], args = url_action[1], kwargs=dict(url_action[2], action = "reset", path = self.compress_path(self.build_path(urlpath))))
            
            stepdata = curdata.get(nextstep.name, {})
            (valid, _, _) = nextstep.get_forms(stepdata)
            
            tplpath.append(("step", {
                'is_on_path': False,
                'is_current': False,
                'is_valid': valid,
                'urls': urls,
                'step': nextstep}))
            
            if nextstep.is_tail(): # restore context
                curdata = curdatastack.pop()
            
            step = nextstep
            nextstep = nextstep.get_straight_branch()
        
        # end while
        
        # OK, we have last step, check if we have stopped because of a branch
        if not step.is_final():
            branches = {}
            for (st, gr) in step.next.itervalues():
                branches[st.name] = {
                    'step': st,
                    'goto': reverse(url_step[0], args = url_step[1], kwargs=dict(url_step[2], path = self.compress_path(self.build_path(urlpath + [(st, 0)]))))
                }
            
            tplpath.append(("branch", branches))
        
        return tplpath

    
    def _fetch_template_cycle(self, cycle, step, hint, cyctx):
        """Rebuild branches"""
        # (is_complete, is_current, urls, [ (step, step), , (branch, ) ])
#        ret = {}
#        i = 1  # skip head
#        while True: # we try to restore the whole path, with hint or without
#            if step.is_head() and i > 1: # first step is always head
#                # fetch nested cycle
#                if step.name not in cyctx: #we don't have cycle data, so we are not complete
#                    return (False, None)
#
#                else:
#                    cycles = cyctx[step.name]
#                    assert isinstance(cycles, list)
#
#                cycldat = [ self._fetch_cycle(step, pt, cyctx) for (pt, cyctx) in cycles ]
#                ret[step.name] = [ cc for (val, cc) in cycldat if val]
#
#                if len(ret[step.name]) < 1: # nested cycle contains no complete cycles, we are not complete too
#                    return (False, None)
#
#                # next from the cycle
#                step = step.cycle.outer_tail
#                if step is None: # cycle is final
#                    return (True, ret)
#
#                # otherwise proceed with next
#                continue
#
#            stepdata = cyctx.get(step.name, {})
#            (valid, stepforms, cleandata) = step.get_forms(stepdata)
#            if not valid:
#                # forget about it, cycle is not valid
#                return (False, None)
#
#            ret[step.name] = stepforms
#
#            if step.is_tail() or step.is_final():
#                return (True, ret)
#
#            # proceed to the next step, use hint
#            # iterator has no has_next(), bad thing
#            expstep = hint[i] if i < len(hint) else None
#            expstep = expstep if expstep is None or isinstance(expstep, CleanStep) else self.steps.get(expstep, None)
#            i += 1
#
#            nextstep = None
#            if expstep is not None:
#                if step.encode_branch(expstep) is not None:
#                    nextstep = expstep
#
#            if expstep is None:
#                # OK, hint is lost or broken, try the first branch
#                nextstep = step.next.itervalues().next() if isinstance(step.next, dict) else step.next
#
#            step = nextstep
        # end of while
        return None


    
    def _fetch_cycle(self, step, hint, cyctx):
        """Fetch single cycle, rebuild path"""
        # OK, we have hint how to rebuild current cycle from cyctx
        # but it is unreliable, it can be empty, shorter/longer than cycle,
        # point to unreachable branches.
        # we have to select only completed valid cycles, current (possibly uncompleted)
        # cycle is handled in refetch_path() directly.
        
        ret = {}
        i = 1  # skip head
        while True: # we try to restore the whole path, with hint or without
            if step.is_head() and i > 1: # first step is always head
                # fetch nested cycle
                if step.name not in cyctx: #we don't have cycle data, so we are not complete
                    return (False, None)
                
                else:
                    cycles = cyctx[step.name]
                    assert isinstance(cycles, list)
                
                cycldat = [ self._fetch_cycle(step, pt, cyctx) for (pt, cyctx) in cycles ]
                ret[step.name] = [ cc for (val, cc) in cycldat if val]
                
                if len(ret[step.name]) < 1: # nested cycle contains no complete cycles, we are not complete too
                    return (False, None)
                
                # next from the cycle
                step = step.cycle.outer_tail
                if step is None: # cycle is final
                    return (True, ret)
                
                # otherwise proceed with next
                continue

            
            stepdata = cyctx.get(step.name, {})
            (valid, stepforms, cleandata) = step.get_forms(stepdata)
            if not valid:
                # forget about it, cycle is not valid
                return (False, None)
            
            ret[step.name] = stepforms
            
            if step.is_tail() or step.is_final():
                return (True, ret)
            
            # proceed to the next step, use hint
            # iterator has no has_next(), bad thing
            expstep = hint[i] if i < len(hint) else None
            expstep = expstep if expstep is None or isinstance(expstep, CleanStep) else self.steps.get(expstep, None)
            i += 1
            
            nextstep = None
            if expstep is not None: # given by hint
                if step.encode_branch(expstep) is not None: # and the hint is really one of the branches
                    nextstep = expstep  # use hint
            
            if nextstep is None:
                # OK, hint is lost or broken, try the first branch
                nextstep = step.next.itervalues().next()[0] if isinstance(step.next, dict) else step.next
            
            step = nextstep
        # end of while

    
    def refetch_path(self, step_path, data, post, files):
        """Restores steps and forms along the path from the data."""
        if len(step_path) == 0:
            step_path.append((self.clean_scenario, 0))
        
        #[FIXME: this is overcomplicated... fixme... =\ ]
        ctx = data
        target = step_path[-1][0]
        last_valid = False
        valid = True
        validpath = []
        wizard_data = {}
        step_context = wizard_data
        path = []
        respath = []
        pathstack = []
        ctxstack = []
        wizctxstack = []
        respathstack = []
        lastforms = None
        for (cidx, (step, cycle)) in enumerate(step_path):
            if step.is_head():
                if step.name not in ctx:
                    cycles = []
                    ctx[step.name] = cycles
                
                else:
                    cycles = ctx[step.name]
                    assert isinstance(cycles, list)
                
                pathstack.append(path)
                ctxstack.append(ctx)
                wizctxstack.append(step_context)
                respathstack.append(respath)
                if cycle >= len(cycles): # create new cycle
                    path = []
                    respath = []
                    ctx = {}
                    cycles.append((path, ctx))
                    cycle = len(cycles) - 1
                    step_path[cidx] = (step, cycle)
                
                else:
                    (respath, ctx) = cycles[cycle]
                    respath.reverse()
                    path = []
                    cycles[cycle] = (path, ctx)

                
                # cleaned context
                newctx = {}
                cycldat = [ self._fetch_cycle(step, pt, cyctx) for (idx, (pt, cyctx)) in enumerate(cycles) if idx != cycle ]
                step_context[step.name] = [ cc for (val, cc) in cycldat if val]
                step_context[step.name].append(newctx)  # current step is always the last
                step_context = newctx
            
            # end if head
            
            if step.name not in ctx:
                stepdata = {}
                ctx[step.name] = stepdata
            
            else:
                stepdata = ctx[step.name]
            
            path.append(step.name)
            if len(respath) > 0:
                respath.pop()
            
            if step is target:
                (last_valid, stepforms, cleandata) = step.get_forms(stepdata, post, files)
                if last_valid: # store back in session
                    ctx[step.name] = cleandata
                    step_context[step.name] = stepforms
                
                lastforms = stepforms
                
                # we will end here, restore the rest of path hint
                # warning: this could be of different branch, we will filter it in next _fetch_cycle/refetch_path
                respathstack.append(respath)
                respathstack.reverse()
                pathstack.append(path)
                for rpt in respathstack:
                    path = pathstack.pop()
                    for rnm in rpt:
                        path.append(rnm)
            
            else:
                (valid, stepforms, cleandata) = step.get_forms(stepdata)
                if valid:
                    step_context[step.name] = stepforms
            
            if step.is_tail() and step is not target:
                path = pathstack.pop()
                respath = respathstack.pop()
                ctx = ctxstack.pop()
                step_context = wizctxstack.pop()
            
            if not valid: # current step is not validated, break here
                break
            
            validpath.append((step, cycle))
        #end of for
        
        return (valid, last_valid, wizard_data, step_context, validpath, lastforms)

    
    def cancel_path(self, step_path, data):
        """Delete cycle at specified path"""
        
        # strange URL... we have not generated it...
        if len(step_path) < 1 or not step_path[-1][0].is_head():
            return step_path # return to original step
        
        ctx = data
        cycles = None
        for (step, cycle) in step_path:
            if step.is_head():
                cycles = ctx.get(step.name, None)
                if not isinstance(cycles, list) or cycle >= len(cycles):
                    break  # cycle doesn't exists already
                
                (pt, ctx) = cycles[cycle]
        
        if cycles is not None and cycle < len(cycles):
            del cycles[cycle]
        
        step_path[-1] = (step_path[-1][0], max(0, len(cycles) - 1) if cycles is not None else 0)
        return step_path

    
    def reset_path(self, step_path, data):
        """Delete data of a specific step"""
        
        if len(step_path) < 1:  # strange... at least initial step is always in
            return step_path
        
        ctx = data
        for (step, cycle) in step_path:
            if step.is_head():
                cycles = ctx.get(step.name, None)
                if not isinstance(cycles, list) or cycle >= len(cycles): # no such data, nothing to drop
                    return step_path
                
                (pt, ctx) = cycles[cycle]
        
        # reset step
        if step.name in ctx:
            del ctx[step.name]
        
        return step_path

    
    def compress_path(self, path):
        """Run-length encoder."""
        return ("".join([ ("%c%d" % (c, len(ss)) if ss[0] != ':' and len(ss) > 2 else ss) for (ss, c) in self.co_path_reg.findall(path)])).lower()

    
    def uncompress_path(self, path):
        """Run-length decoder."""
        return "".join([(ss if len(ct) < 1 else l*int(ct)) for (ss, l, ct) in self.de_path_reg.findall(path.upper())])

    
    def parse_path(self, path):
        """
            Returns tuples (CleanStep, cycle_index) from initial to given step
            by path.
            
            The cycle_index tells you on which cycle you are (index in the list
            of cycles in @wizar_data of corresponding head step).
            
            Note: this method will follow real scenario and stop on first
            inconsistency, returning the valid prefix of the path. If the
            path was not fully parsed, then returned @isvalid will be False.
            
            Syntax of the path:
                path          ::= <cycle_select>? <path_entry>*
                path_entry    ::= <branch_letter> <cycle_select>?
                cycle_select  ::= ':' [0-9]+
                branch_letter ::= [A-Z]
            
            Note: you will have to uncompress_path() if you want to manually
            parse path from URL.
            
            @param path uncompressed path string as obtained from URL
            @return (parsed path, isvalid)
        """
        ret = []
        curstep = self.clean_scenario
        curcycle = 0
        for (branch_letter, cycle, icycle) in self.path_reg.findall(path):
            if icycle != '': # used  normaly by root step only
                curcycle = int(icycle)
                
                if curcycle != 0 and not curstep.is_head():
                    return (ret, False)
            else:
                ret.append((curstep, curcycle))
                curcycle = 0 if cycle == '' else int(cycle)
                
                # fetch next branch
                curstep = curstep.get_branch(branch_letter)
                if curstep is None: # unknown branch, stop at valid prefix
                    return (ret, False)
                
                if curcycle != 0 and not curstep.is_head(): # check if this step is cycled
                    return (ret, False)  # we can not change cycle on non-head step
        
        # end for. if we are here, then everything was OK, append last step
        ret.append((curstep, curcycle))
        return (ret, True)

    
    def build_path(self, curpath = []):
        """
            Build uncompressed URL path from given list of steps. Each entry in
            @curpath list can be a single step or a tuple (step, cycle index, ...)
            The step may be given by name. If path is empty, then path to initial
            step will be build.
            
            The method will validate @curpath against real scenario, on any
            inconsistency with the scenario the method will raise an exception.
            
            Note: you should compress_path() if you want to use the path in URL.
            
            @exception LookupError if curpath is inconsistent with the scenario
            @param curpath list of steps
            @return string path
        """
        curstep = self.clean_scenario
        url = []
        
        for el in curpath:
            if isinstance(el, tuple):
                step = el[0]
                cycle = el[1] if len(el) > 1 else 0
            
            else:
                step = el
                cycle = 0
            
            if not isinstance(step, CleanStep):
                step = self.steps[step]
            
            if step is curstep: # initial step, you may skip it (or repeated step)
                if cycle > 0:
                    if not curstep.is_head():
                        raise LookupError("Can not select cycle %d for step '%s', step is not cycle head!" % (cycle, curstep.name))
                    
                    url.append(':%d' % cycle)
            
            else: # lookup for branch
                letter = curstep.encode_branch(step)
                if letter is None:
                    raise LookupError("No branch '%s' -> '%s' in the scenario" % (curstep.name, step.name))
                
                url.append(letter)
                
                if cycle > 0:
                    if not step.is_head():
                        raise LookupError("Can not select cycle %d for step '%s', step is not cycle head!" % (cycle, step.name))
                    url.append(':%d' % cycle)
                
                curstep = step
        
        # end for
        return "".join(url)

    
    def build_simple_path(self, step):
        """
            Build uncompressed path to given step in a simple scenario.
            
            This method is similar to build_path(), but accepts the CleanStep or
            name of the last step in the path. If scenario doesn't contain any
            cycles or branches, then this method will return the path, otherwise
            an exception will be thrown.
            
            Note: in most cases you want to use this short-cut method instead of
            more advanced build_path().
            
            @exception LookupError if scenario contains cycles or branches
            @param step either CleanStep or step name to which we build the path
            @return string path
        """
        if not isinstance(step, CleanStep):
            step = self.steps[step]
        
        curstep = self.clean_scenario
        path = [curstep]
        while not curstep.is_final() and curstep is not step:
            curstep = curstep.next
            path.append(curstep)
            if not isinstance(curstep, CleanStep):
                raise LookupError("Can ont build simple path to step '%s', step '%s' has multiple branches" % (step.name, curstep.name))
            
            if curstep.is_head() or curstep.is_tail():
                raise LookupError("Can ont build simple path to step '%s', step '%s' is cycled" % (step.name, curstep.name))
        
        if curstep is not step:
            raise LookupError("Weird! Step '%s' is not found in the scenario!" % step.name)
        
        return self.build_path(path)


#==========- Handles session data. override to provide different storage =======
    def handle_files(self, request, *args, **kwargs):
        ret = {}
        for (name, file) in request.FILES.iteritems():
            # [FIXME: exception can be raised, we don't want to simply loos it
            # (with the file) so allow Http500 and logging of this error]
            if settings.WIZARD_UPLOAD_TEMP_DIR:
                (dst, dstpath) = tempfile.mkstemp(suffix = '.upload', dir = settings.WIZARD_UPLOAD_TEMP_DIR)
            else:
                (dst, dstpath) = tempfile.mkstemp(suffix = '.upload')
            
            dstfile = open(dstpath, "wb")
            for chunk in file.chunks():
                dstfile.write(chunk)
            
            dstfile.close()
            os.close(dst)
            
            ret[name] = SessionUploadedFile(dstpath, dstfile, file.content_type, file.size, file.charset)
        
        return ret

    
    def _filter_data(self, dat):
        """Filters data before/after session save/restore."""
        # The data can be:
        #   { name => {form dict} }
        #   { name => [ ([path], {cycle step dicts}) ] }
        #
        # We keep cycle path to know the branches that were taken. The subclass,
        # however, will not get this info in wizard_data and will probably not
        # restore it when editing, so cycle data becomes:
        #   { name => [ {cycle step dicts} ] }
        #
        # We have to restore it to correct form using "first branch" method.
        # The form dicts are:
        #   { form_name => ({data}, {files}) }
        #
        # The content can be in forms if the user has build it may be:
        #   { form_name => FormObject }
        #
        # We have to convert it to:
        #   { form_name => ({cleaned data}, {}) }
        #
        if isinstance(dat, tuple):
            (path, dat) = dat
        else:
            path = []
        
        for (stepname, forms) in dat.items():
            step = self.steps.get(stepname, None)
            if step is None: # ignore unknown data
                del dat[stepname]
                continue
            
            if isinstance(forms, list):  # the step is a nested cycle
                if not step.is_head():  # this is not a cycle, ignore garbage list
                    del dat[stepname]
                    continue
                
                # filter each cycle
                cycles = [ self._filter_data(subdat) for subdat in forms]
                cycles = [ (pt, ctx) for (pt, ctx) in cycles if len(ctx) > 0 ]
                if len(cycles) > 0: # there is some valid data
                    dat[stepname] = cycles
                else:
                    del dat[stepname]
            
            else: # normal step
                for (formname, formdata) in forms.iteritems():
                    if isinstance(formdata, Form):
                        # only validated forms will give their data
                        forms[formname] = (formdata.cleaned_data or {}, {})
                    
                    elif isinstance(formdata, dict): # form data was given as dict
                        forms[formname] = (formdata, {})
                    
                    else: #correct (formdata, files) format. check files
                        (frms, files) = formdata
                        fls = {}
                        for (fk, fd) in files.iteritems():
                            if not fd.failed:
                                fls[fk] = fd
                            
                            #else: is file suddenly removed from temporary dir?
                        
                        if isinstance(frms, Form):
                            forms[formname] = (frms.cleaned_data or {}, fls)
                        else:
                            forms[formname] = (frms, fls)
                
                # end for
                dat[stepname] = forms
        
        # end for
        return (path, dat)

    
    def restore_data(self, request, *args, **kwargs):
        """
            Restore data from the session.
            
            @param request the request object
            @param args positional arguments provided from urls.py
            @param kwargs keyword arguments provided from urls.py
        """
        
        key = "%s_%s" % (self.__class__.__name__, self.name or '')
        ses_id = request.session.get(key, None)
        sess = None
        
        filter = {'complete': False}
        if ses_id is not None:
            filter.update(id = ses_id)
        else: # try to find the last data
            if settings.WIZARD_TIMEOUT:
                filter.update(date__gte = datetime.datetime.now() - settings.WIZARD_TIMEOUT)
            
            filter.update(  user = request.user,
                            wizard_class = self.__class__.__name__,
                            wizard_name = self.name,
                            complete = False,
                         )
        
        try:
            sess = GraphFormWizardSession.objects.filter(**filter).order_by('-date')[0]
        except Exception:
            sess = GraphFormWizardSession.objects.create(user = request.user,
                                                        wizard_class = self.__class__.__name__,
                                                        wizard_name = self.name,
                                                        content = '',
                                                        meta = '',
                                                        complete = False
                                                       )

        
        if sess.content == '':
            data = {}
        else:
            try:
                data = cPickle.loads(str(sess.content))
                
                # we have to check if files are still alive
                (pt, data) = self._filter_data(data)
            
            except Exception:
                # data is tinkered, should not happen, throw it away
                # [FIXME: this could be hard to find bug. better to show a error page here? ]
                data = {}
        
        if sess.meta == '':
            meta = {}
        else:
            try:
                meta = cPickle.loads(sess.meta)
            
            except:
                #[FIXME: logic failure can go unnoticed here...]
                meta = {}
        
        request.session[key] = sess.id
        return (data, meta)

    
    def save_data(self, request, data, meta = {}, *args, **kwargs):
        """
            Save data to the session.
            
            @param request the request object
            @param data the data to save
            @param meta additional dict to save
            @param args positional arguments provided from urls.py
            @param kwargs keyword arguments provided from urls.py
        """
        key = "%s_%s" % (type(self).__name__, self.name or '')
        ses_id = request.session.get(key, None)
        
        (pt, data) = self._filter_data(data)
        content = cPickle.dumps(data)
        meta = cPickle.dumps(meta or {})
        
        try:
            
            sess = GraphFormWizardSession.objects.get(id = ses_id, complete = False)
            sess.content = content
            sess.meta = meta
            sess.save()
        except:
            sess = GraphFormWizardSession.objects.create(
                        user = request.user,
                        wizard_class = self.__class__.__name__,
                        wizard_name = self.name,
                        content = content,
                        meta = meta,
                        complete = False
                    )
        
        request.session[key] = sess.id

    
    def clear_data(self, request, *args, **kwargs):
        """
            When wizard is done, clear session.
            
            @param request the request object
            @param args positional arguments provided from urls.py
            @param kwargs keyword arguments provided from urls.py
        """
        key = "%s_%s" % (self.__class__.__name__, self.name or '')
        ses_id = request.session.get(key, None)
        
        if ses_id is None:  # no data is available, nothing to drop
            return
        
        if not settings.WIZARD_KEEP_DATA:
            GraphFormWizardSession.objects.filter(id = ses_id).delete()
        else:
            GraphFormWizardSession.objects.filter(id = ses_id).update(complete = True)
        
        request.session[key] = None
        del request.session[key]


#================- Override by wizard's base classes -===========
    def revalidation_failed_response(self, request, validpath, step_path,
                                        url_step = ('wizard.step', (), {}),
                                        url_action = ('wizard.action', (), {}),
                                        *args, **kwargs):
        """
            Will be called if path re-validation fails.
            
            Whenever the user sends data to the wizard, the URL will contain
            the path to the step we want to fill. Prior to accepting the data
            the wizard will re-fill/re-validate all steps from initial to the
            requested step along the given path. If not all of them are valid,
            then we can not proceed with the requested step.
            
            There is usually one reason of failure: the session is lost. The
            data collected in previous steps is thus lost. If there is a step
            on the path that requires data (forms validated to False), then
            wizard will stop at that step - the issue should be resolved. This
            can happen if, for example, the user has saved the wizard's URL in
            bookmarks and comes back after logout/login procedure.
            
            By default this method will redirect to the first required step on
            the path. You can override it to provide a page with help message
            and links to other valid steps (to re-start the wizard - go to the
            initial step).
            
            @param request the request object
            @param validpath valid prefix of step_path, can be empty list
            @param step_path the path requested
            @param url_step used to build URL's to steps
            @param url_action uset to build URL's to actions
            @param args positional arguments from urls.py
            @param kwargs named arguments from urls.py
            @return HttpResponse or raise exception
        """
        validurl = self.build_path(validpath)
        return HttpResponseRedirect(reverse(url_step[0], args = url_step[1], kwargs=dict(url_step[2], path = self.compress_path(validurl))))


#================- Override by subclasses -======================
    def wizard_fast_action(self, request, action, step, step_path, *args, **kwargs):
        """
            Handle GET action quickly. By default raises 404.
            
            Similar to wizar_action(), but will be invoked as soon as possible
            without restoring/revalidating all the data. If you don't need
            anything or depend only on the static information about the steps,
            then override this method and register your actions in fast_actions
            class variable.
            
            If you want to edit the existing data, then you should implement
            an (usually "fast") action that may accept arguments and should
            load all of the data as described in done() method. You don't need
            to re-create the forms, use plain dict's instead. When data is
            reconstructed call self.save_data(data, meta, *args, **kwargs)
            to store the data in the session. The meta argument is any dict you
            want to make available in other actions and done() or None if you
            don't use it. Redirect to initial step (eg. self.build_path()).
            The wizard will start with valid data, so user will be able to
            freely jump between steps.
            
            @param request the request object
            @param action the action name as given in URL
            @param step current CleanStep step as requested by URL
            @param step_path current path as returned by parse_path
            @param args positional arguments from urls.py
            @param kwargs keyword arguments from urls.py
            @return HttpResponse generated response
        """
        raise Http404

    
    def wizard_action(self, request, action, meta, step, step_context, step_path, wizard_data, raw_data, *args, **kwargs):
        """
            Invoked on each unrecognized action. By default raises 404.
            
            You can do whatever you like here, you have all the information the
            wizard has. The @action is the action name specified in URL. The
            @meta dict can be used to persistently store some information, that
            will be later available in done() method. The @step, @step_context,
            @step_path and @wizard_data are the same as given to guard_step().
            
            The @raw_data is similar to @wizard_data, but:
                - may contain data of different branches that are not on current path
                - data is stored as simple dict, not in forms
                - data may contain extra meta data (used by the wizard itself)
            
            The @raw_data is thus the session data, that is persistent between
            requests. Often you don't need it unless you want to edit some
            existing object and you want to re-enter the wizard sub-path.
            
            Note: this method is usually overrided for AJAX calls.
            
            @param request request object
            @param action the action name as given in URL
            @param meta meta dictionary for actions, persistent
            @param step current CleanStep step as requested by URL
            @param step_context wizard_data limited to step's cycle (neighboring steps)
            @param step_path current path as returned by parse_path
            @param wizard_data the data from initial up to current step
            @param raw_data data dictionary for steps, persistent
            @param args positional arguments from urls.py
            @param kwargs keyword arguments from urls.py
            @return HttpResponse object or raise exception
        """
        raise Http404

    
    def guard_step(self, request, step, step_context, step_path, wizard_data):
        """
            Default branching logic, used if step has no its own guard.
            If method evaluates to True, then step will be accepted.
            
            To assist your logic you have access to static CleanStep @step object,
            which may not be modified in anyway. You can use its unique name
            together with some external data to make a decision. You can also
            lookup to the satic CleanStep steps in @step_path, which is a list
            of steps returned by parse_path().
            
            Often you will make a decision based on choices made by the user in
            previous steps. The @step_context variable is a dict similar to one
            you will get in done() method, but limited to current cycle only.
            So if you are sitting in a cycle which has a branch and you want to
            lookup in some previous step, then simply:
              - step_context['step name']['form or data name']['fields...']
            
            The @wizard_data is a structure similar to one you will get in done(),
            but contains the data up to current step only. So you can access
            the data of the previous steps, of all other cycles etc.
            The @step_context is a reference to one of the dicts in @wizard_data.
            If your scenario doesn't contain any cycle, then @step_context and
            @wizard_data will be equal.
            
            Note: if all invocations to this method result in False and there
            is no default branch, then error will be raised.
            
            @param request current request
            @param step CleanStep static info about the step (name, forms etc)
            @param step_context wizard_data limited to step's cycle (neighboring steps)
            @param step_path list of CleanStep's from initial step to given @step
            @param wizard_data the data from initial up to current step
            @return bool True to accept this branch, False to skip
        """
        return False

    
    def done(self, request, wizard_data, meta, *args, **kwargs):
        """
            The wizard is done, all forms are validated.
            
            The @wizard_data contains all forms and data properly validated.
            It is a map of:
                { step_name : forms_and_data } -- "sequence" of steps
            or  { step_name => [ { sequence of steps} ] } -- cycle
            
            So to access forms of specific step use:
                wizard_data['step name']['form_or_data_name']['fields...']
            
            If your scenario contains multiple branches, then you can test which
            branch was taken by looking up the step name of the branch in the
            @wizard_data (data of other branches will not be set in @wizard_data).
            
            If step is part of a cycle, then:
                for my_iteration in wizard_data['head step name']:
                    my_iteration['step name']['form_or_data_name']['fields...']
            
            The 'head step name' is the name of the step on which cycle was
            opened. There is always only one head in a cycle. There can be many
            nested cycles, each is a nested list of dicts.
            
            Note: before this method is called the wizard's session was destroyed.
            You should manually re-save wizard_data if you want to re-enter the
            wizard in the same state (why? don't put scenario logic in done()).
            
            @param request the request object
            @param wizard_data scenario data as explained above
            @param meta the extra meta data (your actions may leave data for you here)
            @param args positional arguments from urls.py
            @param kwargs keyword arguments from urls.py
            @return HttpResponse
        """
        raise NotImplementedError("Your %s class has not defined a done() method, which is required." % self.__class__.__name__)



class TestWizard(GraphFormWizard):
    
    scenario = Step("initial", title = "title test") \
                .next('step1') \
                .branch( \
                    Step('step2').cycle() \
                    .next('step3').end() \
                    .next('step4') \
                 ) \
                .branch( \
                    Step('step2b') \
                    .merge('step4'), \
                    True \
                )

    
    def __init__(self, name = None, template = None):
        super(type(self), self).__init__(name, template)