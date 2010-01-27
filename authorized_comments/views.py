from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib import comments
from django.contrib.comments import signals

def flag(request, id):

    if request.user.profile and request.user.profile.type == 'candidate':
        comment = get_object_or_404(comments.get_model(), pk=id)
        comm_model = comment.content_object

        if comm_model.politician.user.id == request.user.id: #Make sure only the politician for which this comment is made can flag

            flag, created = comments.models.CommentFlag.objects.get_or_create(
                comment = comment,
                user    = request.user,
                flag    = comments.models.CommentFlag.SUGGEST_REMOVAL
            )
            signals.comment_was_flagged.send(
                sender  = comment.__class__,
                comment = comment,
                flag    = flag,
                created = created,
                request = request,
            )

    else:
        return HttpResponseForbidden()

    #Redirect back to the page
    if request.META['HTTP_REFERER']:
        return redirect(request.META['HTTP_REFERER'])
    elif comment:
        if comment.content_type.name == 'Goal':
            return redirect('fo.goal', id=comment.object_pk)
        elif comment.content_type.name == 'PoliticianProfile':
            return redirect('fo.politician_comments', id=comment.object_pk)
    else:
        return redirect('fo.home') #Dunno what to do. Going home.


def delete(request, id):

    if request.user.is_staff:
        comment = get_object_or_404(comments.get_model(), pk=id)
        
        flag, created = comments.models.CommentFlag.objects.get_or_create(
            comment = comment,
            user    = request.user,
            flag    = comments.models.CommentFlag.MODERATOR_DELETION
        )
        comment.is_removed = True
        comment.save()
        signals.comment_was_flagged.send(
            sender  = comment.__class__,
            comment = comment,
            flag    = flag,
            created = created,
            request = request,
        )
        
    else:
        return HttpResponseForbidden()

    #Redirect back to the page
    if request.META['HTTP_REFERER']:
        return redirect(request.META['HTTP_REFERER'])
    elif comment:
        if comment.content_type.name == 'Goal':
            return redirect('fo.goal', id=comment.object_pk)
        elif comment.content_type.name == 'PoliticianProfile':
            return redirect('fo.politician_comments', id=comment.object_pk)
    else:
        return redirect('fo.home') #Dunno what to do. Going home.