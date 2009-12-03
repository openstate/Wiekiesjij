"""
    Widgets
"""
import re
from django import forms
from django.utils.translation import ugettext as _



class AddressWidget(forms.widgets.MultiWidget):
    """
        Widget for an address field
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
            forms.widgets.TextInput(attrs={'size': 10}),
            forms.widgets.TextInput(),
        )
        super(AddressWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        if value:
            return value.split(" ", 4)
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