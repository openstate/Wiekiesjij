# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def instance_view(request, instance_id):
    instance = get_object_or_404(ElectionInstance, pk=instance_id)
    return render_to_response('election_instance_view.html', {'instance': instance}, context_instance=RequestContext(request))