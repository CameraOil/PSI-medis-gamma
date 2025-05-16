from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

from datetime import datetime
import json

from .models import Patients, Readings, Nodes
from .forms import PatientForm

def is_allowed(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or user.groups.filter(name=["suster dan dokter", "Admin"]).exists())

@login_required
@user_passes_test(is_allowed)
@permission_required('main_app.view_patients', raise_exception=True)
def index_view(request):
    query = request.GET.get('searchbar')
    if query:
        pasien = Patients.objects.filter(name__icontains=query)
    else:
        pasien = Patients.objects.all().order_by('patient_id')
    return render(request, 'main_app/pasien.html', {'pasiens': pasien})

@login_required
@user_passes_test(is_allowed)
@permission_required('main_app.view_patients', raise_exception=True)
@permission_required('main_app.view_readings', raise_exception=True)
def patient_view(request, pk):
    pasien = Patients.objects.get(pk=pk)
    data_pasien = Readings.objects.filter(patient_id=pasien).order_by('timestamp').reverse()
    nodes = Nodes.objects.all().order_by('pk').reverse()
    # Filter out readings with None BMI
    filtered_data = [d for d in data_pasien if d.bmi is not None]

    # Then get the latest 5 from that
    filtered_data = filtered_data[:5][::-1]

    labels = [d.timestamp.strftime('%b %d') for d in filtered_data]
    bmi_values = [d.bmi for d in filtered_data]

    context ={'pasien': pasien,
              'data': data_pasien, 
              'data_baru': data_pasien.first(),
              'nodes' : nodes,
              'name_json': json.dumps(pasien.name),
              'id_json' : json.dumps(pasien.patient_id),
              'kelamin_json' :json.dumps(pasien.kelamin),
              'contact_json' : json.dumps(pasien.phone_number),
    }

    context.update({
        'labels': json.dumps(labels),
        'bmi_values': json.dumps(bmi_values),
    })

    return render(request, 'main_app/data.html', context)

@login_required
@user_passes_test(is_allowed)
@permission_required('main_app.view_readings', raise_exception=True)
def get_reading_detail(request, reading_id):
    try:
        reading = Readings.objects.get(pk=reading_id)
        data = {
            'berat': reading.berat,
            'tinggi': reading.tinggi,
            'bmi': reading.bmi,
            'urine': reading.urine,
            'temperature': reading.temperature,
            'alcohol': reading.alcohol,
            'urine_display': reading.get_urine_display(),
        }
        return JsonResponse({'success': True, 'data': data})
    except Readings.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Reading not found'})

@login_required
@user_passes_test(is_allowed)
@permission_required('main_app.change_patients', raise_exception=True)
def edit_view(request,pk):
    patient = get_object_or_404(Patients, pk=pk)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            next_url = request.GET.get('pasien_edit')
            if next_url:
                return HttpResponseRedirect(reverse('patient', kwargs={'pk':pk}))
            else:
                return HttpResponseRedirect(reverse('index'))
    else:
        form = PatientForm(instance=patient)

    return render(request, 'main_app/edit.html', {'form': form})    
    # pasien = Patients.objects.get(pk=pk)
    # return render(request, 'main_app/edit.html', {'pasien': pasien})

@login_required
@user_passes_test(is_allowed)
@permission_required('main_app.delete_patients', raise_exception=True)
def delete_patient(request, patient_id):
    if request.POST.get('_method', '').lower() == "delete":
        patient = get_object_or_404(Patients, pk=patient_id)
        patient.delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse(status=405, content="Method not allowed!")

@login_required
@user_passes_test(is_allowed)
@permission_required('main_app.add_patients', raise_exception=True)
def neu_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = PatientForm()
    return render(request, 'main_app/new.html', {'form':form})

@login_required
@permission_required('main_app.view_nodes', raise_exception=True)
def assign_node_view(request):
    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        patient_id = request.POST.get('patient_id')
        node_id = request.POST.get('node_id')

        print("DEBUG:", "patient_id =", patient_id, "| node_id =", node_id)

        if not node_id.strip() or not patient_id.strip():
            return HttpResponseBadRequest("Missing data.")

        # Do your assignment logic here:
        # e.g., mark the node as assigned or link to a user
        try:
            patient = get_object_or_404(Patients, pk = patient_id)
            node = get_object_or_404(Nodes, pk=node_id)
            if node.status == 'available':
                timestamp = datetime.now()
                node.status = 'assigned'
                node.assigned_patient = patient
                node.assigned_at = timestamp
                

                Readings.objects.create(patient_id=patient, node=node, timestamp=timestamp)
                node.save()
                return JsonResponse({"status": "assigned", "node_id": node_id})  # Replace with your actual success redirect
            else:
                return HttpResponse("Node is not available.", status=400)
        except Nodes.DoesNotExist:
            return HttpResponse("Node not found.", status=404)
    else:
        return HttpResponseBadRequest("Unsupported method override.")
    
