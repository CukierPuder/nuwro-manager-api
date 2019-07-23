from rest_framework import serializers

from core.models import Experiment, Measurement


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
