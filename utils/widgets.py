"""
    Widgets
"""
import re
import datetime
from django import forms
from django.utils.dates import MONTHS
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
			<label for="middle-name">%(middle_name_label)s <span class="optional">%(optional_text)s</span></label>
			%(middle_name_field)s
		</div>
		<div class="first-name text field">
			<label for="first-name">%(first_name_label)s</label>
			%(first_name_field)s
		</div>
    """
    
    def __init__(self, *args, **kwargs):
        max_lengths = kwargs.pop('max_lengths', [80, 15, 65])
        widgets = (
            forms.widgets.TextInput(attrs={'maxlength': max_lengths[0]}),
            forms.widgets.TextInput(attrs={'maxlength': max_lengths[2]}),
            forms.widgets.TextInput(attrs={'maxlength': max_lengths[1]}),
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
            
            optional_text = _('optional'),
            
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
    TEMPLATE = u"""
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
        self.items = model.objects.values_list(field, flat=True).distinct().order_by(field)


    def render(self, *args, **kwargs):
        html_id = kwargs.get('attrs', {}).get('id', '')
        data = u", ".join(self.items)
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
            jQuery(document).ready(function() {
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

            jQuery('#%(id)s_preview').ColorPicker({

                onShow: function (colpkr) {
                    $(colpkr).fadeIn(500);
                    return false;
                },
                onHide: function (colpkr) {
                    $(colpkr).fadeOut(500);
                    return false;
                },
                onBeforeShow: function () {
                    $(this).ColorPickerSetColor($('#%(id)s').val());
                },
                onChange: function (hsb, hex, rgb) {
                    $('#%(id)s_preview').css('backgroundColor', '#' + hex);
                    $('#%(id)s').val(hex);
                }

            })
            .bind('click', function(){
                $(this).ColorPickerSetColor($('#%(id)s').value);
            });

            jQuery(document).ready(function(){
                $('#%(id)s_preview').css('backgroundColor', '#' + $('#%(id)s').val());
                $('#%(id)s').addClass("colorpicker_inputfield");
            });
            }); //end of document.ready
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


class SelectTimeWidget(forms.widgets.Widget):
    """
    A Widget that splits time input into <select> elements.
    Allows form to show as 24hr: <hour>:<minute>:<second>,
    or as 12hr: <hour>:<minute>:<second> <am|pm> 
    
    Also allows user-defined increments for minutes/seconds
    """
    hour_field = '%s_hour'
    minute_field = '%s_minute'
    second_field = '%s_second' 
    meridiem_field = '%s_meridiem'
    twelve_hr = False # Default to 24hr.
    
    time_pattern = r'(\d\d?):(\d\d)(:(\d\d))? *([aApP]\.?[mM]\.?)?$' # w/ Magus's suggestions

    RE_TIME = re.compile(time_pattern)
    # The following are just more readable ways to access re.matched groups:
    HOURS = 0
    MINUTES = 1
    SECONDS = 3
    MERIDIEM = 4
    
    TEMPLATE = """
        <div class="%(type)s select field">
            <label for="%(id)s">%(label)s</label>
            %(field)s
        </div>
    """
    
    
    def __init__(self, attrs=None, hour_step=None, minute_step=None, second_step=None, twelve_hr=False, hide_seconds=True):
        '''
        hour_step, minute_step, second_step are optional step values for
        for the range of values for the associated select element
        twelve_hr: If True, forces the output to be in 12-hr format (rather than 24-hr)
        '''
        self.attrs = attrs or {}
        
        if twelve_hr:
            self.twelve_hr = True # Do 12hr (rather than 24hr)
            self.meridiem_val = 'a.m.' # Default to Morning (A.M.)
        
        if hour_step and twelve_hr:
            self.hours = range(1,13,hour_step) 
        elif hour_step: # 24hr, with stepping.
            self.hours = range(0,24,hour_step)
        elif twelve_hr: # 12hr, no stepping
            self.hours = range(1,13)
        else: # 24hr, no stepping
            self.hours = range(0,24) 

        if minute_step:
            self.minutes = range(0,60,minute_step)
        else:
            self.minutes = range(0,60)

        if second_step:
            self.seconds = range(0,60,second_step)
        else:
            self.seconds = range(0,60)
            
        self.hide_seconds = hide_seconds

    def render(self, name, value, attrs=None):
        try: # try to get time values from a datetime.time object (value)
            hour_val, minute_val, second_val = value.hour, value.minute, value.second
            if self.twelve_hr:
                if hour_val >= 12:
                    self.meridiem_val = 'p.m.'
                else:
                    self.meridiem_val = 'a.m.'
        except AttributeError:
            hour_val = minute_val = second_val = 0
            if isinstance(value, basestring):
                match = self.RE_TIME.match(value)
                if match:
                    time_groups = match.groups();
                    hour_val = int(time_groups[self.HOURS]) % 24 # force to range(0-24)
                    minute_val = int(time_groups[self.MINUTES]) 
                    if time_groups[self.SECONDS] is None:
                        second_val = 0
                    else:
                        second_val = int(time_groups[self.SECONDS])
                    
                    # check to see if meridiem was passed in
                    if time_groups[self.MERIDIEM] is not None:
                        self.meridiem_val = time_groups[self.MERIDIEM]
                    else: # otherwise, set the meridiem based on the time
                        if self.twelve_hr:
                            if hour_val >= 12:
                                self.meridiem_val = 'p.m.'
                            else:
                                self.meridiem_val = 'a.m.'
                        else:
                            self.meridiem_val = None
                    

        # If we're doing a 12-hr clock, there will be a meridiem value, so make sure the
        # hours get printed correctly
        if self.twelve_hr and self.meridiem_val:
            if self.meridiem_val.lower().startswith('p') and hour_val > 12 and hour_val < 24:
                hour_val = hour_val % 12
        elif hour_val == 0:
            hour_val = 12
            
        output = []
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        # NOTE: for times to get displayed correctly, the values MUST be converted to unicode
        # When Select builds a list of options, it checks against Unicode values
        hour_val = u"%.2d" % hour_val
        minute_val = u"%.2d" % minute_val
        second_val = u"%.2d" % second_val

        hour_choices = [("%.2d"%i, "%.2d"%i) for i in self.hours]
        local_attrs = self.build_attrs(id=self.hour_field % id_)
        select_html = forms.widgets.Select(choices=hour_choices).render(self.hour_field % name, hour_val, local_attrs)
        output.append(self.TEMPLATE % {
            'label': _('Hours'),
            'field': select_html,
            'id': local_attrs.get('id'),
            'type': 'hours',
        })

        minute_choices = [("%.2d"%i, "%.2d"%i) for i in self.minutes]
        local_attrs['id'] = self.minute_field % id_
        select_html = forms.widgets.Select(choices=minute_choices).render(self.minute_field % name, minute_val, local_attrs)
        output.append(self.TEMPLATE % {
            'label': _('Minutes'),
            'field': select_html,
            'id': local_attrs.get('id'),
            'type': 'minutes',
        })
        
        if not self.hide_seconds:
            second_choices = [("%.2d"%i, "%.2d"%i) for i in self.seconds]
            local_attrs['id'] = self.second_field % id_
            select_html = forms.widgets.Select(choices=second_choices).render(self.second_field % name, second_val, local_attrs)
            output.append(self.TEMPLATE % {
                'label': _('Seconds'),
                'field': select_html,
                'id': local_attrs.get('id'),
                'type': 'seconds',
            })
    
        if self.twelve_hr:
            #  If we were given an initial value, make sure the correct meridiem get's selected.
            if self.meridiem_val is not None and  self.meridiem_val.startswith('p'):
                    meridiem_choices = [('p.m.','p.m.'), ('a.m.','a.m.')]
            else:
                meridiem_choices = [('a.m.','a.m.'), ('p.m.','p.m.')]

            local_attrs['id'] = self.meridiem_field % id_
            select_html = forms.widgets.Select(choices=meridiem_choices).render(self.meridiem_field % name, self.meridiem_val, local_attrs)
            output.append(self.TEMPLATE % {
                'label': _('Am/Pm'),
                'field': select_html,
                'id': local_attrs.get('id'),
                'type': 'ap_pm',
            })

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_time' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        # if there's not h:m:s data, assume zero:
        h = data.get(self.hour_field % name, 0) # hour
        m = data.get(self.minute_field % name, 0) # minute 
        s = data.get(self.second_field % name, '00') # second
  

        meridiem = data.get(self.meridiem_field % name, None)

        #NOTE: if meridiem IS None, assume 24-hr
        if meridiem is not None:
            if meridiem.lower().startswith('p') and int(h) != 12:
                h = (int(h)+12)%24 
            elif meridiem.lower().startswith('a') and int(h) == 12:
                h = 0
        
        if (int(h) == 0 or h) and m and s:
            return '%s:%s:%s' % (h, m, s)

        return data.get(name, None)

class DateTimePicker(forms.widgets.MultiWidget):
    """
        This class combines SelectTimeWidget (see above)
        and A DateInput for date selection
        Adds jquery datepicker for extra functionality
    """
    
    TEMPLATE = """
        <div class="date text field">
            <label for="%(id)s">%(label)s</label>
            %(field)s
        </div>
        <script type="text/javascript">
        <!--
            jQuery(document).ready(function(){
                // Making the date picker
                jQuery('#%(id)s').datepicker({dateFormat: $.datepicker.W3C});
            });
        -->
        </script>
    """
    
    def __init__(self, attrs=None, format=None, hour_step=None, minute_step=5, second_step=None, twelve_hr=None, hide_seconds=True):
        """
            Parameters for widgets
        """
        widgets = (
            forms.widgets.DateInput(attrs=attrs, format=format),
            SelectTimeWidget(attrs=attrs, hour_step=hour_step, minute_step=minute_step, second_step=second_step, twelve_hr=twelve_hr, hide_seconds=hide_seconds),
        )
        super(DateTimePicker, self).__init__(widgets, attrs)
        
        
        
    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]
    
    def render(self, name, value, attrs=None):
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            if i == 1:                
                output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
            else:
                output.append(self.TEMPLATE % {
                    'label': _('Date'),
                    'field': widget.render(name + '_%s' % i, widget_value, final_attrs),
                    'id': final_attrs.get('id'),
                })
        return mark_safe(self.format_output(output))
    
class HiddenDateTimePicker(DateTimePicker):
    def __init__(self, *args, **kwargs):
        super(HiddenDateTimePicker, self).__init__(*args, **kwargs)

        self.widgets = (
            forms.widgets.HiddenInput(),
            forms.widgets.HiddenInput(),
        )
    
    def render(self, name, value, attrs=None):
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)

        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            if i == 1:                
                output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
            else:
                output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
        return mark_safe(self.format_output(output))

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

class DateSelectPicker(forms.widgets.Widget):
    
    """
    A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    FULL_TEMPLATE = """
        <div class="day field select">
            <label for="%(day_id)s">%(day_label)s</label>
            %(day)s
        </div>
        <div class="month field select">
            <label for="%(month_id)s">%(month_label)s</label>
            %(month)s
        </div>
        <div class="year field select">
            <label for="%(year_id)s">%(year_label)s</label>
            %(year)s
        </div>
    """
    
    DAYLESS_TEMPLATE = """
        %(day)s
        <div class="month field select">
            <label for="%(month_id)s">%(month_label)s</label>
            %(month)s
        </div>
        <div class="year field select">
            <label for="%(year_id)s">%(year_label)s</label>
            %(year)s
        </div>
    """
    
    RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')
    none_value = (0, '---')
    month_field = '%s_month'
    day_field = '%s_day'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True, fixed_day=None):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)
            
        if type(fixed_day) == int:
            self.fixed_day = fixed_day
        else:
            self.fixed_day = None

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, basestring):
                match = self.RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = {}

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
            
        local_attrs = self.build_attrs(id=self.day_field % id_)
        if self.fixed_day is not None:
            s = forms.widgets.HiddenInput()
            hidden_html = s.render(self.day_field % name, self.fixed_day, local_attrs)
            output.update({'day': hidden_html})
        else:
            day_choices = [(i, i) for i in range(1, 32)]
            if not (self.required and value):
                day_choices.insert(0, self.none_value)
            s = forms.widgets.Select(choices=day_choices)
            select_html = s.render(self.day_field % name, day_val, local_attrs)
            output.update({'day': select_html})
    
        month_choices = MONTHS.items()
        if not (self.required and value):
            month_choices.append(self.none_value)
        month_choices.sort()
        local_attrs['id'] = self.month_field % id_
        s = forms.widgets.Select(choices=month_choices)
        select_html = s.render(self.month_field % name, month_val, local_attrs)
        output.update({'month': select_html})

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, self.none_value)
        local_attrs['id'] = self.year_field % id_
        s = forms.widgets.Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.update({'year': select_html})
        
        
        #labels
        output.update({
            'day_label': _('Day'),
            'month_label': _('Month'),
            'year_label': _('Year'),
        })
        #ids
        output.update({
            'day_id': self.day_field % id_,
            'month_id': self.month_field % id_,
            'year_id': self.year_field % id_,
        })
        if self.fixed_day is None:
            return mark_safe(self.FULL_TEMPLATE % output)
        return mark_safe(self.DAYLESS_TEMPLATE % output)

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if self.fixed_day and m == y == "0":
            return None
        if y == m == d == "0":
            return None
        if y and m and d:
            return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)
    

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
