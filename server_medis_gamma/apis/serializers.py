from rest_framework import serializers
from main_app.models import Patients, Readings, Nodes

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = '__all__'

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Readings
        fields = '__all__'

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodes
        fields = '__all__'
