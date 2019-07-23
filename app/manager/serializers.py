from rest_framework import serializers

from core.models import Experiment


class ExperimentSerializer(serializers.ModelSerializer):
    """Serializer for Experiment objects"""

    class Meta:
        model = Experiment
        fields = ('id', 'name')
        read_only_fields = ('id',)
