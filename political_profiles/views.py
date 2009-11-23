# Create your views here.

def get_profile(request):
    
    print request.user.get_profile()
    
    return