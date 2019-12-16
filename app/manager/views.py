import os

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Experiment,
    Measurement,
    Nuwroversion,
    Artifact,
    Resultfile
)
from manager import serializers


def generate_artifact_link(experiment_name,
                           measurement_name,
                           nuwroversion_name,
                           resultfile_name,
                           artifact_name):
    """Generate filepath for new artifact file"""
    return os.path.join((
        f'media/uploads/artifacts'
        f'/{experiment_name}'
        f'/{measurement_name}'
        f'/{nuwroversion_name}'
        f'/{resultfile_name.split(".")[0]}'),
        artifact_name
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
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin):
    """Base viewset for Experiment, Measurement and Nuwroversion"""
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


class ResultfileViewSet(viewsets.ModelViewSet):
    """Manage resultfile in the database"""
    serializer_class = serializers.ResultfileSerializer
    queryset = Resultfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the Resultfiles"""
        experiment_str = self.request.query_params.get('experiment')
        measurement_str = self.request.query_params.get('measurement')

        if experiment_str and measurement_str:
            experiment_instance = Experiment.objects.get(
                pk=int(experiment_str)
            )
            measurement_instance = Measurement.objects.get(
                pk=int(measurement_str)
            )

            return Resultfile.objects.filter(
                experiment__name=experiment_instance.name,
                measurement__name=measurement_instance.name
            )

        return Resultfile.objects.all()

    def get_serializer_class(self):
        """Return apropriate serializer class"""
        if self.action == 'list':
            return serializers.ResultfileListSerializer
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


class ArtifactViewSet(viewsets.ModelViewSet):
    """Manage artifacts in database"""
    serializer_class = serializers.ArtifactSerializer
    queryset = Artifact.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the artifacts for the authenticated user"""
        if self.request.query_params.get('resultfile'):
            return Artifact.objects.filter(resultfile__pk=int(self.request.query_params.get('resultfile')))
        return Artifact.objects.all()

    def get_serializer_class(self):
        """Return the apropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.ArtifactDetailSerializer
        return serializers.ArtifactSerializer

    def perform_create(self, serializer):
        """Create new object and save file in FS"""
        resultfile = Resultfile.objects.get(pk=int(self.request.data['resultfile']))
        serializer.save(
            resultfile=resultfile,
            filename=self.request.data['filename'],
            link=generate_artifact_link(
                resultfile.experiment.name,
                resultfile.measurement.name,
                resultfile.nuwroversion.name,
                resultfile.filename,
                self.request.data['filename']
            )
        )
