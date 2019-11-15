from rest_framework import serializers

from core.models import (
    Experiment,
    Measurement,
    Nuwroversion,
    Datafile,
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
            'id', 'experiment', 'measurement', 'variable',
            'filename', 'input_file', 'link', 'creation_date')
        read_only_fields = ('id', 'filename', 'link', 'creation_date')
        extra_kwargs = {
            'input_file': {'write_only': True}
        }


class DatafileListSerializer(serializers.ModelSerializer):
    experiment = ExperimentSerializer()
    measurement = MeasurementSerializer()

    class Meta:
        model = Datafile
        fields = ('id', 'experiment', 'measurement', 'variable',
                  'filename', 'link', 'creation_date')


class DatafileDetailSerializer(DatafileSerializer):
    """Serializer for a Datafile detail"""
    experiment = ExperimentSerializer(read_only=True)
    measurement = MeasurementSerializer(read_only=True)


class ResultfileListSerializer(serializers.ModelSerializer):
    experiment = ExperimentSerializer(read_only=True)
    measurement = MeasurementSerializer(read_only=True)
    nuwroversion = NuwroversionSerializer(read_only=True)
    related_datafiles = DatafileDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Resultfile
        fields = ('id', 'experiment', 'measurement', 'nuwroversion', 'is_3d',
                  'description', 'x_axis', 'y_axis', 'filename', 'link',
                  'related_datafiles', 'creation_date')


class ResultfileSerializer(serializers.ModelSerializer):
    """Serializer for Datafile objects"""
    experiment = serializers.PrimaryKeyRelatedField(
        queryset=Experiment.objects.all()
    )
    measurement = serializers.PrimaryKeyRelatedField(
        queryset=Measurement.objects.all()
    )
    nuwroversion = serializers.PrimaryKeyRelatedField(
        queryset=Nuwroversion.objects.all()
    )
    related_datafiles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Datafile.objects.all()
    )

    class Meta:
        model = Resultfile
        fields = (
            'id', 'experiment', 'measurement', 'nuwroversion', 'is_3d',
            'description', 'x_axis', 'y_axis', 'filename', 'result_file',
            'related_datafiles', 'link', 'creation_date'
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
    related_datafiles = DatafileDetailSerializer(read_only=True, many=True)
