import os

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Experiment,
    Measurement,
    Nuwroversion,
    Datafile,
    Resultfile
)
from manager import serializers


def generate_datafile_link(experiment_name, measurement_name, filename):
    """Generate filepath for new Datafile file"""

    return os.path.join(
        f'media/uploads/datafiles/{experiment_name}/{measurement_name}/',
        filename
    )


def generate_resultfile_link(experiment_name,
                             measurement_name,
                             nuwroversion_name,
                             filename):
    """Generate filepath for new Resultfile file"""
    return os.path.join((
        f'media/uploads/resultfiles'
        f'/{experiment_name}'
        f'/{measurement_name}'
        f'/{nuwroversion_name}'),
        filename
    )


class BaseFileAttrViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin):
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
        """Retrieve the datafiles for the authenticated user"""
        return self.queryset

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
            link=generate_datafile_link(
                experiment_instance.name,
                measurement_instance.name,
                filename
            )
        )


class ResultfileViewSet(viewsets.ModelViewSet):
    """Manage resultfile in the database"""
    serializer_class = serializers.ResultfileSerializer
    queryset = Resultfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the Resultfiles"""
        return self.queryset

    def get_serializer_class(self):
        """Return apropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.ResultfileDetailSerializer
        return serializers.ResultfileSerializer

    def perform_create(self, serializer):
        """Create a new object"""
        filename = self.request.data['result_file'].name
        experiment_instance = Experiment.objects.get(
            pk=int(self.request.data['experiment']))
        measurement_instance = Measurement.objects.get(
            pk=int(self.request.data['measurement']))
        nuwroversion_instance = Nuwroversion.objects.get(
            pk=int(self.request.data['nuwroversion']))

        serializer.save(
            filename=filename,
            link=generate_resultfile_link(
                experiment_instance,
                measurement_instance,
                nuwroversion_instance,
                filename
            )
        )
