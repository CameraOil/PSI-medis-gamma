from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponseForbidden

def is_allowed(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or user.groups.filter(name=["Dokter", "Suster","Admin"]).exists())

@login_required
@user_passes_test(is_allowed)
def index_view(request):
    return render(request, 'main_app/index.html')
