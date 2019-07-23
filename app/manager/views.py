from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Experiment, Measurement
from manager import serializers


class ExperimentViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Manage experiments in database"""
    queryset = Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return the list of all objects"""
        return self.queryset.order_by('-name')


class MeasurementViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """Manage measurements in database"""
    queryset = Measurement.objects.all()
    serializer_class = serializers.MeasurementSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return the list of all objects ordered by name"""
        return self.queryset.order_by('-name')
