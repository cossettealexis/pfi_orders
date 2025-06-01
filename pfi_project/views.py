from django.shortcuts import redirect

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('user_login')