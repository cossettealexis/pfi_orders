from django.shortcuts import redirect

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to dashboard if logged in
    return redirect('user_login')  # Redirect to login if not logged in