from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from main_app.models import Patients, Readings, Nodes
from .serializers import PatientSerializer, ReadingSerializer, NodeSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Readings.objects.all()
    serializer_class = ReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def latest(self, request):
        node_id = request.query_params.get("node_id")
        if not node_id:
            return Response({"error": "node_id is required"}, status=400)

        try:
            reading = Readings.objects.filter(node__id=node_id).latest("timestamp")
            return Response({"id": reading.pk,
                             "patient": reading.patient_id.pk,
                             "timestamp": reading.timestamp})
        except Readings.DoesNotExist:
            return Response({"error": "No reading found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Nodes.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [permissions.IsAuthenticated]
