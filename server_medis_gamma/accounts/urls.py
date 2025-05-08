from django.urls import path

from .views import StaffLoginView

urlpatterns = [
    path('login/', StaffLoginView.as_view(), name='staff-login')
]
