"""
Holds widgets
"""
import utils
import re
from django.forms import widgets
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from itertools import chain
from django.utils.html import conditional_escape
from django.utils.datastructures import MultiValueDict, MergeDict
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

class ReadOnlyWidget(forms.Widget):
    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs, name=name)
        if hasattr(self, 'initial'):
            value = self.initial
        return mark_safe("<input %s disabled='%s' value='%s' />" % (flatatt(final_attrs), 'disabled', value or ''))
        #return "%s" % (flatatt(final_attrs), value or '')

    def _has_changed(self, initial, data):
        return False

class ReadOnlyField(forms.FileField):
    """
    Extend the FileField

    This is done because of how the clean method works for this kind of field.
    """
    widget = ReadOnlyWidget
    def __init__(self, widget=None, label=None, initial=None, help_text=None):
        forms.Field.__init__(self, label=label, initial=initial,
            help_text=help_text, widget=widget)

    def clean(self, value, initial):
        self.widget.initial = initial
        return initial



def clean_valid_bankaccount(numstr):
    """
        Checks if given number is valid using elfproof check (valid for Dutch banks).
        Function returns None if account number is invalid or number if check
        succeeds
    """

    # strip all non digits (-, p etc)
    acc = re.sub("[^0-9]", "", numstr)
    # account number is 10 digits (requirement DNB etc)
    # however 10th digit is always 0, must be elfproof anyway

    # elfproof
    if re.match('^[0-9]{9,10}$', acc):
        sm = 0
        for pos,let in enumerate(acc):
            sm += int(let) * (9 - pos)

        return acc if (sm % 11) == 0 else None

    # postbank number
    acc = re.sub("^0+", "", acc)
    return ("p%s" % acc) if (len(acc) >= 3 and len(acc) <= 7) else None



class DutchBankAccountField(forms.fields.CharField):
    """
    Validates input against elfproof check.
    """

    default_error_messages = {
        'invalid': _(u'Enter valid bankaccount number.'),
    }

    def clean(self, value):
        val = clean_valid_bankaccount(super(DutchBankAccountField, self).clean(value))
        if val is None:
            raise forms.ValidationError(self.error_messages['invalid'])

        return val

class SelectiveCheckboxSelectMultiple(widgets.SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label, editable) in enumerate(chain(self.choices, choices)):
            if editable:
                # If an ID attribute was given, add a numeric index as a suffix,
                # so that the checkboxes don't all have the same ID attribute.
                if has_id:
                    final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                    label_for = u' for="%s"' % final_attrs['id']
                else:
                    label_for = ''

                cb = widgets.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
                option_value = force_unicode(option_value)
                rendered_cb = cb.render(name, option_value)
                option_label = conditional_escape(force_unicode(option_label))
                output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
            else: # non editable option
                output.append(u'<li>[Default] %s</li>' % option_label)

        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            ret = []
            ls = set(data.getlist(name))
            for i, (v, l, editable) in enumerate(chain(self.choices)):
                if not editable or unicode(v) in ls:
                    ret.append(v)

            return ret

        return data.get(name, None)


class PermissionListWidget(widgets.MultiWidget):
    """
    Widget that renders permission choices as a tree.
    """

    def __init__(self, attrs=None, display_permissions = {}, groups_default_permissions = {}, groups_available_permissions = {}, template = None):
        self.groups_available_permissions = utils.get_permissions_for_group(groups_available_permissions)
        self.groups_default_permissions  = utils.get_permissions_for_group(groups_default_permissions)
        self.display_permissions = display_permissions

        boxes = []
        avail = set(self.groups_available_permissions)
        defaul = set(self.groups_default_permissions)
        # this sucks, but needs to be only on edit page, so not a problem
        for (app, (label, models)) in self.display_permissions.items():
            for model in models:
                choices = []
                conts = ContentType.objects.filter(app_label = app, model = model.lower())
                perms = Permission.objects.select_related().filter(content_type__in = conts)

                for p in perms:
                    if p in avail:
                        if p in defaul: # always available, not editable
                            choices.append((p.pk, p.name, False))
                        else: # editable choices
                            choices.append((p.pk, p.name, True))

                boxes.append(SelectiveCheckboxSelectMultiple(attrs = attrs, choices = choices))


        self.count_boxes = len(boxes)
        self.template = template
        super(PermissionListWidget, self).__init__(boxes, attrs)


    def render(self, name, value, attrs=None):
        val = [value for i in range(self.count_boxes)]

        return super(PermissionListWidget, self).render(name, val, attrs)


    def value_from_datadict(self, data, files, name):
        vals = super(PermissionListWidget, self).value_from_datadict(data, files, name)
        ret = []
        for val in vals:
            if val:
                ret.extend(val)

        return ret

    def format_output(self, rendered_widgets):
        """Render widgets"""
        if self.template is not None:
            ret = []
            tr = iter(rendered_widgets)
            for (app, (label, models)) in self.display_permissions.items():
                sub = {}
                for model in models:
                    sub[model] = tr.next()
                ret.append((app, label, sub))

            return render_to_string(self.template, {'schema': self.display_permissions, 'widgets': rendered_widgets, 'tree': ret})
        else:
            return super(PermissionListWidget, self).format_output(rendered_widgets)



