from django.contrib.auth.views import LoginView
from .forms import EmailLoginForm

class StaffLoginView(LoginView):
    authentication_form = EmailLoginForm
    template_name = 'accounts/login.html'
