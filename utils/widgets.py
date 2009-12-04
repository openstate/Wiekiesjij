"""
    Widgets
"""
import re
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

class AddressWidget(forms.widgets.MultiWidget):
    """
        Widget for an address field bit
    """
    
    TEMPLATE = """
        <div class="fields">
            <table>
                <tr>
                    <td colspan="2">%(street_label)s</td>
                    <td>%(number_label)s</td>
                </tr>
                <tr>
                    <td colspan="2">%(street_field)s</td>
                    <td>%(number_field)s</td>
                </tr>
                <colgroup span="1" align="left"></colgroup>
                <colgroup span="2"></colgroup>
                <tr>
                    <td>%(post_label)s</td>
                    <td colspan="2">%(city_label)s</td>
                </tr>
                <tr>
                    <td>%(post_field)s</td>
                    <td colspan="2">%(city_field)s</td>
                </tr>
            </table>
        </div>"""
    
    def __init__(self, attrs=None):
        widgets = (
            forms.widgets.TextInput(),
            forms.widgets.TextInput(attrs={'size': 10}),
            forms.widgets.TextInput(attrs={'size': 7}),
            forms.widgets.TextInput(),
        )
        super(AddressWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        if value:
            matches = value.match("^(.+) (\d+.*) (\d+.*) (.+)$", value)
            return [matches.group(1), matches.group(2), matches.group(3), matches.group(4)]
        else:
            return [None, None, None, None]
        
    def format_output(self, rendered_widgets):
        return self.TEMPLATE % dict(
            street_label = _('Street'),
            number_label = _('Number'),
            post_label = _('Postcode'),
            city_label = _('City'),
            street_field = rendered_widgets[0], 
            number_field = rendered_widgets[1],
            post_field = rendered_widgets[2],
            city_field = rendered_widgets[3]
        )
        
        
class NameWidget(forms.widgets.MultiWidget):
    """
        Widget to fill out a name
    """
    TEMPLATE = """
        <div class="fields">
            <table>
                <tr>
                    <td>%(first_name_label)s</td>
                    <td>%(last_name_label)s</td>
                </tr>
                <tr>
                    <td>%(first_name_field)s</td>
                    <td>%(last_name_field)s</td>
                <tr>
                    <td>&nbsp;</td>
                    <td>%(middle_name_label)s</td>
                </tr>
                <tr>
                    <td>&nbsp;</td>
                    <td>%(middle_name_field)s</td>
                </tr>
            </table>
        </div>
    """
    
    def __init__(self, attrs=None):
        widgets = (
            forms.widgets.TextInput(),
            forms.widgets.TextInput(),
            forms.widgets.TextInput(),
        )
        super(NameWidget, self).__init__(widgets, attrs)
        
    def decompress(self, value):
        if value:
            return value.split(' ', 3)
        else:
            return [None, None, None] 
        
    def format_output(self, rendered_widgets):
        return self.TEMPLATE % dict(
            first_name_label = _('First name'),
            last_name_label = _('Last name'),
            middle_name_label = _('Middle name'),
            
            first_name_field = rendered_widgets[0],
            last_name_field = rendered_widgets[1],
            middle_name_field = rendered_widgets[2],
        )
    
    
class AutoCompleter(forms.widgets.TextInput):
    """ 
        Auto completer 
    """
    CLIENT_CODE = """
        <script type="text/javascript">
             jQuery(document).ready(function(){
                jQuery('#%(id)s').autocomplete("%(data)s".split(', '), {max: %(limit)d});
             });
        </script>
    """
    
    class Media:
        js = (
            'static/utils/javascripts/jquery.autocomplete.min.js',
        )
        css = {
            'screen': (
                'static/utils/css/autocomplete.css',
            ),
        }
    
        
    def __init__(self, model, field, *args, **kwargs):
        super(AutoCompleter, self).__init__(*args, **kwargs)
        self.items = model.objects.values_list(field, flat=True).order_by(field)


    def render(self, *args, **kwargs):
        html_id = kwargs.get('attrs', {}).get('id', '')
        data = ", ".join(self.items)
        limit = 15

        result = super(AutoCompleter, self).render(*args, **kwargs)

        return result + mark_safe(self.CLIENT_CODE % dict(id=html_id, data=data, limit=limit))