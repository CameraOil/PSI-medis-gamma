from django.contrib.auth.views import LoginView
from .forms import EmailLoginForm
#Aku nggak tau ini buat apa tapi seharusnya kalau ada ini bakalan bisa
# kalau nggak ada bakalan rusak
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Override to use email instead of username
        request.data['username'] = request.data.get('email')
        return super().post(request, *args, **kwargs)


class StaffLoginView(LoginView):
    authentication_form = EmailLoginForm
    template_name = 'accounts/login.html'