from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from frontoffice.models import VisitorResult
from elections.models import Council
from elections.forms import SmsEventForm
from sms.models import sendsms

def events(request, council_id):
    council = get_object_or_404(Council, id=council_id)
    events = council.events.all()

    parent = 'frontoffice/iframe.html'
  
    returndict = {'council': council, 'parent':parent, }

      
    #check for sms module
  
    if request.method == 'POST':
        form = SmsEventForm(queryset=council.events.all(), data=request.POST)
        if form.is_valid():
            if form.cleaned_data['value']:
                events = form.cleaned_data['value']
                returndict['events'] = events
            if form.cleaned_data['phone_number']:
                phone_number = form.cleaned_data['phone_number']
                returndict['phone_number'] = phone_number
            #message = 'hi ber'
            for event in events:
                #result = sendsms(event.originator, phone_number, message, event.event_datetime)
                event.sms_subscriptions.create(phone_number=phone_number)
  
            return render_to_response('elections/events_result.html', returndict, context_instance=RequestContext(request))
        else:
            print 'test'
    else:
        form = SmsEventForm(queryset=council.events.all(),empty_label=None)
   

    returndict['form'] = form

    return render_to_response('elections/events.html', returndict, context_instance=RequestContext(request))

