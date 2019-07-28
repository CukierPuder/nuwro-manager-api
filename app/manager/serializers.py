from rest_framework import serializers

from core.models import (
    Experiment,
    Measurement,
    Nuwroversion,
    Datafile
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


class DatafileSerializer(serializers.ModelSerializer):
    """Serializer for Datafile objects"""
    experiment = serializers.PrimaryKeyRelatedField(
        queryset=Experiment.objects.all()
    )
    measurement = serializers.PrimaryKeyRelatedField(
        queryset=Measurement.objects.all()
    )

    class Meta:
        model = Datafile
        fields = (
            'id', 'experiment', 'measurement', 'variable', 'x_axis',
            'y_axis', 'filename', 'input_file', 'link')
        read_only_fields = ('id', 'filename', 'link')
        extra_kwargs = {
            'input_file': {'write_only': True}
        }


class DatafileDetailSerializer(DatafileSerializer):
    """Serializer for a Datafile detail"""
    experiment = ExperimentSerializer(read_only=True)
    measurement = MeasurementSerializer(read_only=True)
