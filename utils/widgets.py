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
    
    def __init__(self, *args, **kwargs):
        widgets = (
            forms.widgets.TextInput(),
            forms.widgets.TextInput(attrs={'size': 10}),
            forms.widgets.TextInput(attrs={'size': 7}),
            forms.widgets.TextInput(),
        )
        kwargs.update({
            'widgets': widgets,
        })
        super(AddressWidget, self).__init__(*args, **kwargs)
    
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
        
class HiddenAddressWidget(AddressWidget):
    
    def __init__(self, *args, **kwargs):
        super(HiddenAddressWidget, self).__init__(*args, **kwargs)
        
        self.widgets = (
            forms.widgets.HiddenInput(),
            forms.widgets.HiddenInput(),
            forms.widgets.HiddenInput(),
            forms.widgets.HiddenInput(),
        )
        
    def format_output(self, rendered_widgets):
        return "\n".join(rendered_widgets)
        
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
    
    def __init__(self, *args, **kwargs):
        widgets = (
            forms.widgets.TextInput(),
            forms.widgets.TextInput(),
            forms.widgets.TextInput(),
        )
        kwargs.update({
            'widgets': widgets,
        })
        super(NameWidget, self).__init__(*args, **kwargs)
        
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
    
class HiddenNameWidget(NameWidget):

    def __init__(self, *args, **kwargs):
        super(HiddenNameWidget, self).__init__(*args, **kwargs)

        self.widgets = (
            forms.widgets.HiddenInput(),
            forms.widgets.HiddenInput(),
            forms.widgets.HiddenInput(),
            forms.widgets.HiddenInput(),
        )

    def format_output(self, rendered_widgets):
        return "\n".join(rendered_widgets)
        
        
        
class AutoCompleter(forms.widgets.TextInput):
    """ 
        Auto completer 
    """
    TEMPLATE = """
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

        return result + mark_safe(self.TEMPLATE % dict(id=html_id, data=data, limit=limit))

class ColorPicker(forms.widgets.TextInput):
    """
        Color Picker
    """
    TEMPLATE = """
        <!-- Following div could need CSS -->
        <div class="cp_preview" id="%(id)s_preview" style="height: 20px; width: 20px;"></div>
        <script type="text/javascript">
            jQuery('#%(id)s').ColorPicker({

                onShow: function (colpkr) {
                    $(colpkr).fadeIn(500);
                    return false;
                },
                onHide: function (colpkr) {
                    $(colpkr).fadeOut(500);
                    return false;
                },
                onBeforeShow: function () {
                    $(this).ColorPickerSetColor(this.value);
                },
                onChange: function (hsb, hex, rgb) {
                    $('#%(id)s_preview').css('backgroundColor', '#' + hex);
                    $('#%(id)s').val(hex);
                }

            })
            .bind('keyup', function(){
                $(this).ColorPickerSetColor(this.value);
            });

            jQuery(document).ready(function(){
                $('#%(id)s_preview').css('backgroundColor', '#' + $('#%(id)s')[0].value);
            });

        </script>
    """

    class Media:
        js = (
            'static/utils/javascripts/colorpicker.js',
        )
        css = {
            'screen': (
                'static/utils/css/colorpicker.css',
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ColorPicker, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        html_id = kwargs.get('attrs', {}).get('id', '')
        result = super(ColorPicker, self).render(*args, **kwargs)

        return result + mark_safe(self.TEMPLATE % dict(id=html_id))