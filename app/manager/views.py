from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Experiment, Measurement, Nuwroversion
from manager import serializers


class BaseFileAttrViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    """Base viewset for DataFile and ResultFile"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return the list of all objects ordered by name"""
        return self.queryset.order_by('-name')


class ExperimentViewSet(BaseFileAttrViewSet):
    """Manage experiments in database"""
    queryset = Experiment.objects.all()
    serializer_class = serializers.ExperimentSerializer


class MeasurementViewSet(BaseFileAttrViewSet):
    """Manage measurements in database"""
    queryset = Measurement.objects.all()
    serializer_class = serializers.MeasurementSerializer


class NuwroversionViewSet(BaseFileAttrViewSet):
    """Manage nuwroversions in database"""
    queryset = Nuwroversion.objects.all()
    serializer_class = serializers.NuwroversionSerializer
