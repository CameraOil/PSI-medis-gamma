from rest_framework import serializers
from main_app.models import Patients, Readings, Nodes

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = '__all__'

class ReadingSerializer(serializers.ModelSerializer):
    urine_display = serializers.SerializerMethodField(method_name='get_urine_display')
    class Meta:
        model = Readings
        fields = '__all__'  # or list of fields you want

    def get_urine_display(self, obj):
        return obj.get_urine_display()

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodes
        fields = '__all__'
