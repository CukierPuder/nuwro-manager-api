from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Measurement
from manager.serializers import MeasurementSerializer


MEASUREMENTS_URL = reverse('manager:measurement-list')


class PublicMeasurementApiTests(TestCase):
    """Test publicly available measurements API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving measurements"""
        res = self.client.get(MEASUREMENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMeasurementApiTests(TestCase):
    """Test the authorized user measurements API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_measurements(self):
        """Test retrieving measurements"""
        Measurement.objects.create(name='CC0pi')
        Measurement.objects.create(name='PP0ci')

        res = self.client.get(MEASUREMENTS_URL)
        measurements = Measurement.objects.all().order_by('-name')
        serializer = MeasurementSerializer(measurements, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_measurement_successful(self):
        """Test creating new measurement"""
        payload = {'name': 'CC0pi'}
        self.client.post(MEASUREMENTS_URL, payload)
        exists = Measurement.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_invalid_measurement(self):
        """Test creating a new measurement with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(MEASUREMENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
