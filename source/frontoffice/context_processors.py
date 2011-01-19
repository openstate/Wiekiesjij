
def homepage_placeholder(request):
    from django.conf import settings
    return {'HOMEPAGE_PLACEHOLDER': settings.HOMEPAGE_PLACEHOLDER}