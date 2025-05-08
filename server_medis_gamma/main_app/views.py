from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from .models import Patients
from .forms import PatientForm

def is_allowed(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or user.groups.filter(name=["Dokter", "Suster","Admin"]).exists())

@login_required
@user_passes_test(is_allowed)
def index_view(request):
    query = request.GET.get('searchbar')
    if query:
        pasien = Patients.objects.filter(name__icontains=query)
    else:
        pasien = Patients.objects.all()
    return render(request, 'main_app/pasien.html', {'pasiens': pasien})

@login_required
@user_passes_test(is_allowed)
def patient_view(request,pk):
    pasien = Patients.objects.get(pk=pk)
    return render(request, 'main_app/data.html', {'pasien': pasien})

@login_required
@user_passes_test(is_allowed)
def edit_view(request,pk):
    pasien = Patients.objects.get(pk=pk)
    return render(request, 'main_app/edit.html', {'pasien': pasien})

@login_required
@user_passes_test(is_allowed)
def delete_patient(request, patient_id):
    if request.POST.get('_method', '').lower() == "delete":
        patient = get_object_or_404(Patients, pk=patient_id)
        patient.delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse(status=405, content="Method not allowed!")

@login_required
@user_passes_test(is_allowed)
def neu_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = PatientForm()
    return render(request, 'main_app/new.html', {'form':form})


