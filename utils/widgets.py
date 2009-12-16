"""
    Widgets
"""
import re
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.forms.widgets import RadioSelect

            
class AddressWidget(forms.widgets.MultiWidget):
    """
        Widget for an address field bit
    """
    
    TEMPLATE = """
		<div class="street text field">
			<label for="street">%(street_label)s</label>
			%(street_field)s
		</div>
		<div class="number text field">
			<label for="number">%(number_label)s</label>
			%(number_field)s
		</div>
		<div class="postcode text field">
			<label for="street">%(post_label)s</label>
			%(post_field)s
		</div>
		<div class="city text field">
			<label for="street">%(city_label)s</label>
			%(city_field)s
		</div>
        """
    
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
        if value and isinstance(value, dict):
            return [value.get('street'), value.get('number'), value.get('postalcode'), value.get('city')]
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
        <div class="last-name text field">
			<label for="last-name">%(last_name_label)s</label>
			%(last_name_field)s
		</div>
		<div class="middle-name text field">
			<label for="middle-name">%(middle_name_label)s <span class="optional">optional</span></label>
			%(middle_name_field)s
		</div>
		<div class="first-name text field">
			<label for="first-name">%(first_name_label)s</label>
			%(first_name_field)s
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
        if value and isinstance(value, dict):
            return [value.get('first_name'), value.get('last_name'), value.get('middle_name')]
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
                $('#%(id)s').addClass("colorpicker_inputfield");
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

class DateTimePicker(forms.widgets.TextInput):
    """
    DateTime Picker, based on jQuery UI and "jquery.jtimepicker.js".
    It uses jQuery UI dor date picking and jTimePicker class for date picking.
    
    Example of usage:
        class MyForm(forms.Form):
            my_date_time = forms.DateTimeField(max_length=50)

            def __init__(self, *args, **kwargs):
                super(self.__class__, self).__init__(*args, **kwargs)
                self.fields['my_date_time'].widget = DateTimePicker()
        
    """
    TEMPLATE = """
        <script type="text/javascript">
        <!--
            jQuery(document).ready(function(){
                date_obj = new Date();
                date_obj_hours = date_obj.getHours();
                date_obj_mins = date_obj.getMinutes();

                if (date_obj_mins < 10) {
                    date_obj_mins = "0" + date_obj_mins;
                }
                date_obj_time = date_obj_hours + ':' + date_obj_mins;

                // Getting the element
                var datePicker = jQuery('#%(id)s');

                // Making another hidden element for date
                var datePickerField = jQuery('<input type="hidden" value="" id="#%(id)s_date"/>');

                // Giving it the same name as our element
                datePickerField.attr('name', datePicker.attr('name'));

                // Saving the original date time value
                originalDateTimeValue = datePicker.attr('value');

                // Splitting the original date time value to get date and time separately
                originalDateTimeSplit = originalDateTimeValue.split(' ', 2);
                try {
                    originalDateValue = originalDateTimeSplit[0];
                    originalTimeValue = originalDateTimeSplit[1];
                    originalTimeValueSplit = originalTimeValue.split(':', 3);
                    originalTimeValueHours = originalTimeValueSplit[0];
                    originalTimeValueMinutes = originalTimeValueSplit[1];
                    originalTimeValueSeconds = parseInt(originalTimeValueSplit[2]);
                    originalDateTimeValue = originalDateValue + ' ' + originalTimeValueHours + ':' + originalTimeValueMinutes + ':' + originalTimeValueSeconds;
                } catch (err) {
                    originalDateValue = '';
                    originalTimeValue = '';
                    originalTimeValueHours = 0;
                    originalTimeValueMinutes = 0;
                    originalTimeValueSeconds = 0;
                }

                // Changing the name of the original field
                datePicker.attr('name', datePicker.attr('name') + '_original');

                // Making another div container for the time picking
                var timePickerField = jQuery('<div class="time-picker" id="#%(id)s_time"></div>');
                
                // Adding the elements
                datePicker.after(timePickerField);
                datePicker.after(datePickerField);

                // Copying the value of time to the time element
                datePicker.attr('value', originalDateValue);
                datePickerField.attr('value', originalDateTimeValue);
                
                // Making the date picker
                datePicker.datepicker({dateFormat: $.datepicker.W3C});

                // Making the time picker
                timePickerField.jtimepicker({'hourDefaultValue': originalTimeValueHours,
                                             'minDefaultValue': originalTimeValueMinutes,
                                             'secDefaultValue': originalTimeValueSeconds});

                // Time picker elements
                timePickerFieldHours = jQuery('select.hourcombo');
                timePickerFieldMinutes = jQuery('select.mincombo');
                timePickerFieldSeconds = jQuery('select.seccombo');
                timePickerFieldSeconds.hide();

                timePickerFieldHours.before(jQuery('<label>%(hours_label)s</label>'));
                timePickerFieldMinutes.before(jQuery('<label>%(minutes_label)s</label>'));
                //timePickerFieldSeconds.before(jQuery('<label>%(seconds_label)s</label>'));

                // Updating the full date and time value on date picker change
                datePicker.change(function() {
                    datePickerField.attr('value', getDateTimeValue(datePicker, timePickerFieldHours, timePickerFieldMinutes, timePickerFieldSeconds));
                });

                // Updating the full date and time value on time picker change
                timePickerFieldHours.change(function() {
                    datePickerField.attr('value', getDateTimeValue(datePicker, timePickerFieldHours, timePickerFieldMinutes, timePickerFieldSeconds));
                });

                // Updating the full date and time value on time picker change
                timePickerFieldMinutes.change(function() {
                    datePickerField.attr('value', getDateTimeValue(datePicker, timePickerFieldHours, timePickerFieldMinutes, timePickerFieldSeconds));
                });

                // Updating the full date and time value on time picker change
                timePickerFieldSeconds.change(function() {
                    datePickerField.attr('value', getDateTimeValue(datePicker, timePickerFieldHours, timePickerFieldMinutes, timePickerFieldSeconds));
                });
            });
        -->
        </script>
    """

    class Media:
        js = (
            'static/utils/javascripts/jquery.jtimepicker.js',
        )
        css = {
            'screen': (
                'static/utils/css/jquery.timepicker.css',
            ),
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        html_id = kwargs.get('attrs', {}).get('id', '')
        result = super(self.__class__, self).render(*args, **kwargs)

        return result + mark_safe(self.TEMPLATE % dict(id=html_id,
                                                       hours_label=_('Hours'),
                                                       minutes_label=_('Minutes'),
                                                       seconds_label=_('Seconds')))


class DatePicker(forms.widgets.TextInput):
    """
    Date Picker, based on jQuery UI.
    It uses jQuery UI dor date picking.

    Example of usage:
        class MyForm(forms.Form):
            my_date_time = forms.DateTimeField(max_length=50)

            def __init__(self, *args, **kwargs):
                super(self.__class__, self).__init__(*args, **kwargs)
                self.fields['my_date_time'].widget = DatePicker()

    """
    TEMPLATE = """
        <script type="text/javascript">
        <!--
            jQuery(document).ready(function(){
                // Making the date picker
                jQuery('#%(id)s').datepicker({dateFormat: $.datepicker.W3C});
            });
        -->
        </script>
    """

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        html_id = kwargs.get('attrs', {}).get('id', '')
        result = super(self.__class__, self).render(*args, **kwargs)

        return result + mark_safe(self.TEMPLATE % dict(id=html_id))


class RadioRating(RadioSelect):
    '''
        Rating widget based on RadioSelect widget. Displays values from 1 to 10.
    '''
    def render(self, name, value, attrs=None, choices=()):
        # Creating a list of values from 1 to 10
        choices = map(lambda x: (x, x), range(1, 11))
        return self.get_renderer(name, value, attrs, choices).render()


class RadioBoolean(RadioSelect):
    '''
        Boolean widget widget based on RadioSelect widget.
    '''
    def render(self, name, value, attrs=None, choices=()):
        # Creating a list of values from 1 to 10
        choices = (('', _('Unknown')), (True, _('Yes')), (False, _('No')))
        return self.get_renderer(name, value, attrs, choices).render()
