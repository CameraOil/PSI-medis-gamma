from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from accounts.views import CustomObtainAuthToken

urlpatterns = [
    path('accounts/', include('accounts.urls')),  # login, register, etc.
    path('', include('main_app.urls')),           # index page, protected
    path('admin/', admin.site.urls),
    path('api/', include('apis.urls')),
    path('api-token-auth/', CustomObtainAuthToken.as_view(), name='api_token_auth'),
]

