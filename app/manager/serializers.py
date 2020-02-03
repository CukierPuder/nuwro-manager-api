from rest_framework import serializers

from core.models import (
    Experiment,
    Measurement,
    Nuwroversion,
    Artifact,
    Resultfile
)


class ExperimentSerializer(serializers.ModelSerializer):
    """Serializer for Experiment objects"""

    class Meta:
        model = Experiment
        fields = ('id', 'name')
        read_only_fields = ('id',)


class MeasurementSerializer(serializers.ModelSerializer):
    """Serializer for Measurement objects"""

    class Meta:
        model = Measurement
        fields = ('id', 'name')
        read_only_fields = ('id',)


class NuwroversionSerializer(serializers.ModelSerializer):
    """Serializer for Nuwroversion objects"""

    class Meta:
        model = Nuwroversion
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ResultfileListSerializer(serializers.ModelSerializer):
    experiment = ExperimentSerializer(read_only=True)
    measurement = MeasurementSerializer(read_only=True)
    nuwroversion = NuwroversionSerializer(read_only=True)

    class Meta:
        model = Resultfile
        fields = ('id', 'experiment', 'measurement', 'nuwroversion', 'is_3d',
                  'description', 'x_axis', 'y_axis', 'filename', 'link',
                  'creation_date')


class ResultfileSerializer(serializers.ModelSerializer):
    """Serializer for Resultfile objects"""
    experiment = serializers.PrimaryKeyRelatedField(
        queryset=Experiment.objects.all()
    )
    measurement = serializers.PrimaryKeyRelatedField(
        queryset=Measurement.objects.all()
    )
    nuwroversion = serializers.PrimaryKeyRelatedField(
        queryset=Nuwroversion.objects.all()
    )

    def create(self, validated_data):
        instance = Resultfile.objects.create(**validated_data)
        instance.link = instance.result_file.path.replace('/vol/web/', '')
        instance.save()

        return instance

    class Meta:
        model = Resultfile
        fields = (
            'id', 'experiment', 'measurement', 'nuwroversion', 'is_3d',
            'description', 'x_axis', 'y_axis', 'filename', 'result_file',
            'link', 'creation_date'
        )
        read_only_fields = ('id', 'filename', 'link')
        extra_kwargs = {
            'result_file': {'write_only': True}
        }


class ResultfileDetailSerializer(ResultfileSerializer):
    """Serializer for a Resultfile detail"""
    experiment = ExperimentSerializer(read_only=True)
    measurement = MeasurementSerializer(read_only=True)
    nuwroversion = NuwroversionSerializer(read_only=True)


class ArtifactSerializer(serializers.ModelSerializer):
    resultfile = serializers.PrimaryKeyRelatedField(
        queryset=Resultfile.objects.all()
    )

    def create(self, validated_data):
        instance = Artifact.objects.create(**validated_data)
        instance.link = instance.artifact.path.replace('/vol/web/', '')
        instance.save()
        return instance

    class Meta:
        model = Artifact
        fields = ('id', 'resultfile', 'filename', 'artifact', 'link', 'addition_date')
        read_only_fields = ('id', 'filename', 'link', 'addition_date')
        extra_kwargs = {
            'artifact': {'write_only': True}
        }


class ArtifactDetailSerializer(ArtifactSerializer):
    resultfile = ResultfileDetailSerializer
