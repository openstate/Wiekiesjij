"""
FormWizard class -- implements a multi-page form, validating between each
step and storing the form's state as HTML hidden fields so that no state is
stored on the server side.

This is an extended version which allows display of multiple forms per step and
take different branches between steps.

Author: Sardar Yumatov (ja.doma@gmail.com)

Based on: http://www.djangosnippets.org/snippets/1514/
Which is based on: django.contrib.formtools.FormWizard
"""

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _
from django import forms as djangoforms

from django.contrib.formtools.utils import security_hash



class Step(object):
    """Single page, single step."""

    def __init__(self, name, **kwargs):
        """
        Create new step, the name must be unique in the tree.

        @param name unique name of this step(page)
        @param kwargs: dict(
            forms = dict( #list of forms for this page as name => form_class
                    form        = Form1,
                    linkform    = Form2,
                ),

            # optional
            prefixes = dict( # name => prefix; if not set, then name is used
                    form     = 'main_form',
                    linkform = 'link_form',
                ),

            # optional
            initial = dict( # initial value (dict, model object, query set etc)
                    form     = None,
                    linkform = None,
                ),

            # optional extra content, will be passed to step template
            extra_context = dict(),
            
            form_kwargs = dict( #kwargs to pass to the form on contrsuction
                form_name = {'question_id': 10}
            )

            # specific template for this step, optional
            template = 'foo/bar.html'
        )
        """

        self.name = name
        self.forms = kwargs.get('forms')
        self.prefixes = kwargs.get('prefixes', {})
        self.initial = kwargs.get('initial', {})
        self.form_kwargs = kwargs.get('form_kwargs', {})
        self.template = kwargs.get('template')
        self.extra_context = kwargs.get('extra_context', {})
        
        self._next = []


    def next(self, *args):
        """Define next steps/branches. Returns self."""
        self._next.extend(args)
        return self

            
    def validate_unique(self, steps):
        """Ensure all names are unique, find all nodes."""
        
        if self.name in steps:
            raise KeyError("Duplicate step name: %s" % self.name)

        steps.update({self.name: self})

        for step in self._next:
            if isinstance(step, Step):
                step.validate_unique(steps)


    def validate_resolve(self, steps, cycle):
        """Resolve all named references"""
        
        if self.name in cycle:
            raise ValueError("Cyclic scenario detected, step '%s' is entered twice" % self.name)

        cycle.add(self.name)
        for i, step in enumerate(self._next):
            if not isinstance(step, Step):
                nx = steps.get(step)
                if nx is None:
                    raise KeyError("Step with name '%s' is not defined" % step)

                self._next[i] = nx
                nx.validate_resolve(steps, cycle)
            else:
                step.validate_resolve(steps, cycle)

        cycle.remove(self.name)


    def get_branch(self, idx):
        """Returns child step by index"""
        return self._next[idx]
        

    def get_forms(self, data = None, files = None):
        """Returns all defined forms, populated with data"""
        
        forms = dict()

        for name, form in self.forms.iteritems():
            kwargs = self.get_form_kwargs(name)
            # model form
            if hasattr(form, 'Meta') and hasattr(form.Meta, 'model'):
                init = 'instance'
            # management form
            elif hasattr(form, 'management_form'):
                init = 'queryset'
            # normal form (initialized from dictionary)
            else:
                init = 'initial'

            kwargs.update({
                init : self.initial.get(name),
                'prefix' : self.get_prefix(name),
                'data': data,
                'files': files,
            })

            f = form(**kwargs)
            forms.update({name : f})

        return forms
    
    def get_form_kwargs(self, form_name):
        return self.form_kwargs.get(form_name, {})

    def get_prefix(self, form_name):
        """Returns the prefix for a form"""
        
        return u'%s_%s' % (
            self.name,
            self.prefixes.get(form_name)
        ) if self.prefixes.get(form_name) else  u'%s_%s' % (
            self.name,
            form_name
        )


    def is_leaf(self):
        return len(self._next) == 0


    def next_steps(self):
        return [step.name for step in self._next]



class MultiPathFormWizard(object):
    """Multi-path form wizard."""
    
    # The HTML (and POST data) field name for the "step" variable.
    step_field_name = "wizard_step"
    
    # encoding used for branches, single letter
    branch_code = ''.join([chr(i) for i in xrange(ord('A'), ord('Z')+1)])

    
    def __init__(self, steps_tree, template = None):
        """ 
            Create new wizard.

            @param steps_tree the wizard scenario
            @param template default template for all steps
        """
        steps = {}
        steps_tree.validate_unique(steps)
        steps_tree.validate_resolve(steps, set())

        self.steps_tree = steps_tree
        self.template = template


    def __call__(self, request, *args, **kwargs):
        # list of processed steps with current step in tail
        (str_path, current_path) = self.determine_path(request, *args, **kwargs)

        # allow the subclass to initialize any extra state if needed
        self.parse_params(request, *args, **kwargs)

        # restore hashed data or fail to broken step
        (stat, forms_path) = self.restore_previous_forms(request, current_path[:-1], str_path[:-1])
        if not stat:
            # if restoration failed (hash failure)
            return forms_path

        # Process the current step. If it's valid, go to next step or done()
        cur_step = current_path[-1]
        if request.method == 'POST':
            
            # the last step may take files as parameter
            forms = cur_step.get_forms(request.POST, request.FILES)
        else:
            forms = cur_step.get_forms()
        
        valid = True
        for name, form in forms.iteritems():
            valid &= form.is_valid()
    
        forms_path.append(forms)
        
        # current set of forms is valid, allow next step
        # note: empty form can be valid if no required fields are there, so ensure
        # POST
        if request.method == 'POST' and valid:
            # notify next step is complete
            self.process_step(request, forms_path, current_path)

            if not cur_step.is_leaf():
                # index of the next branch
                branch = self.get_next_step(request, current_path[-1].next_steps(), current_path, forms_path)
                # if extending class returns wrong branch, then KeyError here
                next_step = current_path[-1].get_branch(branch)
                

                current_path.append(next_step)
                forms_path.append(next_step.get_forms())
                str_path += MultiPathFormWizard.branch_code[branch]
            else:
                # OK, wizard is completed, revalidate forms
                ret = {}
                for i, forms in enumerate(forms_path):
                    if not all([form.is_valid() for (_, form) in forms.iteritems()]):
                        return self.render_revalidation_failure(request, current_path[:i+1], forms_path[:i+1], str_path[:i])
                    else:
                        ret[current_path[i].name] = forms

                return self.done(request, ret)

        context = kwargs.get('extra_context', {})
        return self.render(request, current_path, forms_path, str_path, context)



    def determine_path(self, request, *args, **kwargs):
        """
        Given the request object and whatever *args and **kwargs were passed to
        __call__(), returns the current chain of steps taken.
        """
        if not request.POST:
            # initial steps if opened for the first time
            return ("", [self.steps_tree])

        steps = [self.steps_tree]
        key = []
        try:
            step = str(request.POST.get(self.step_field_name, ""))
            node = self.steps_tree
            for l in step:
                node = node.get_branch(MultiPathFormWizard.branch_code.index(l))
                steps.append(node)
                key.append(l)
        except:
            # user tinkered with the data, ignore, we will continue from valid step
            pass

        return (''.join(key), steps)


    def restore_previous_forms(self, request, current_path, str_path):
        """Verify hash and restore data"""
        path = []
        for i, step in enumerate(current_path):
            forms = step.get_forms(request.POST)
            path.append(forms)
            for name, form in forms.iteritems():
                form.full_clean()
                if request.POST.get('hash_%s_%s' % (step.name, name), '') != self.security_hash(request, form):
                    return (False, self.render_hash_failure(request, current_path[:i+1], path, str_path[:i]))

        return (True, path)


    def render(self, request, step_path, forms_path, str_path, context = {}):
        "Renders the given step path, returning an HttpResponse."
        old_data = request.POST or {}
        prev_fields = []
        
        hidden = djangoforms.HiddenInput()
        # Collect all data from previous steps and render it as HTML hidden fields.
        for i, forms in enumerate(forms_path[:-1]):
            step = step_path[i]
            for name, form in forms.iteritems():
                hash_name = u'hash_%s_%s' % (step.name, name)
                prev_fields.extend([field.as_hidden() for field in form])
                prev_fields.append(
                    hidden.render(
                        hash_name,
                        old_data.get(
                            hash_name,
                            self.security_hash(request, form)
                        )
                    )
                )

        return self.render_template(request, forms_path[-1], ''.join(prev_fields), str_path, step_path[-1], context)


    # METHODS SUBCLASSES MIGHT OVERRIDE IF APPROPRIATE ########################

    def render_hash_failure(self, request, step_path, forms_path, str_path):
        """
        Hook for rendering a template if a hash check failed.

        All steps in step_path except the last one are guaranteed to be valid.
        The forms_path contains all valid forms except the last one.
        The str_path contains the string encoded path to current failing step.

        This default implementation simply renders the form for the given step,
        but subclasses may want to display an error message, etc.
        """
        return self.render(
            request,
            step_path, # all steps including the last broken
            forms_path, # all forms including the last broken
            str_path, # string path to broken step
            context = dict(
                wizard_error = _('We apologize, but your form has expired. Please continue filling out the form from this page.')
            )
        )

    def render_revalidation_failure(self, request, step_path, forms_path, str_path):
        """
        Hook for rendering a template if final revalidation failed.

        It is highly unlikely that this point would ever be reached, but See
        the comment in __call__() for an explanation.
        """
        return self.render(
            request,
            step_path, # all steps including the last broken
            forms_path, # all forms including the last broken
            str_path, # string path to broken step
            context = dict(
                wizard_error = _('We apologize, but your form is lost because of unknown reason. Please continue filling out the form from this page.')
            )
        )

    def security_hash(self, request, form):
        """
        Calculates the security hash for the given HttpRequest and Form instances.

        Subclasses may want to take into account request-specific information,
        such as the IP address.
        """

        return security_hash(request, form)

    def parse_params(self, request, *args, **kwargs):
        """
        Hook for setting some state, given the request object and whatever
        *args and **kwargs were passed to __call__(), sets some state.

        This is called at the beginning of __call__().
        """
        pass

    def get_template(self, step):
        """
        Hook for specifying the name of the template to use for a given step.

        Note that this can return a tuple of template names if you'd like to
        use the template system's select_template() hook.
        """
        if step.template:
            return step.template

        if self.template:
            return self.template

        raise ValueError('Please provide a template')


    def render_template(self, request, forms, previous_fields, str_path, step, context = {}):
        """
        Renders the template for the given step, returning an HttpResponse object.

        Override this method if you want to add a custom context, return a
        different MIME type, etc. If you only need to override the template
        name, use get_template() instead.

        The template will be rendered with the following context:
            step_field -- The name of the hidden field containing the step path
            step       -- The current step object
            step_path  -- The string path to current step
            forms      -- The dictionary with forms
            previous_fields -- A string representing every previous data field,
                          plus hashes for completed forms, all in the form of
                          hidden fields. Note that you'll need to run this
                          through the "safe" template filter, to prevent
                          auto - escaping, because it's raw HTML.
        """
        context = context or {}
        context.update(step.extra_context)
        return render_to_response(self.get_template(step), dict(context,
            step_field = self.step_field_name,
            step = step,
            step_path = str_path,
            forms = forms,
            previous_fields = previous_fields
        ), context_instance = RequestContext(request))


    def process_step(self, request, forms_path, current_path):
        """
        Hook for modifying the wizard's internal state, given a fully
        validated path of forms up to current step. All forms in forms_path
        are guaranteed to contain valid data.

        This method should * not * modify any of that data. Rather, it might want
        to set self.extra_context, based on previously submitted forms.

        Note that this method is called every time a page is rendered for * all *
        submitted steps.
        """
        pass

    # METHODS SUBCLASSES MUST OVERRIDE ########################################
    def get_next_step(self, request, next_steps, current_path, forms_path):
        """
            Returns *index* of the next step the wizard should go.
            The current_path[-1] is the current node, the next_steps is the list
            of names of possible next steps. Your code should look up in:

                forms_path[specific steps][specific_forms].cleaned_data

            to determine the name of the next step and return next_steps.index(name).
        """
        raise NotImplementedError("Your %s class has not defined a get_next_step() method, which is required." % self.__class__.__name__)


    def done(self, request, form_dict):
        """
        Hook for doing something with the validated data. This is responsible
        for the final processing.

        The form_dict is a dictionary step_name => forms containing all valid
        forms for completed wizard path.
        """
        raise NotImplementedError("Your %s class has not defined a done() method, which is required." % self.__class__.__name__)
