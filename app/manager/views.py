import os

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Experiment, Measurement, Nuwroversion, Datafile
from manager import serializers


def generate_file_link(experiment_name, measurement_name, filename):
    """Generate filepath for new Datafile file"""

    return os.path.join(
        f'media/uploads/datafiles/{experiment_name}/{measurement_name}/',
        filename
    )


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


class DatafileViewSet(viewsets.ModelViewSet):
    """Manage datafiles in the database"""
    serializer_class = serializers.DatafileSerializer
    queryset = Datafile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return apropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.DatafileDetailSerializer

        return serializers.DatafileSerializer

    def perform_create(self, serializer):
        """Create a new object"""
        filename = self.request.data['input_file'].name
        experiment_instance = Experiment.objects.get(
            pk=int(self.request.data['experiment'])
        )
        measurement_instance = Measurement.objects.get(
            pk=int(self.request.data['measurement'])
        )
        serializer.save(
            filename=filename,
            link=generate_file_link(
                experiment_instance.name,
                measurement_instance.name,
                filename
            )
        )
