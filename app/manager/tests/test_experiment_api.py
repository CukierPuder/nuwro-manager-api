from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Experiment
from manager.serializers import ExperimentSerializer


EXPERIMENTS_URL = reverse('manager:experiment-list')


class PublicExperimentApiTests(TestCase):
    """Test the publicly available xperiments API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(EXPERIMENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateExperimentApiTests(TestCase):
    """Test the authorized user experiments API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_experiments(self):
        """Test retrieving experiments"""
        Experiment.objects.create(name='MINERvA')
        Experiment.objects.create(name='MINERvB')

        res = self.client.get(EXPERIMENTS_URL)
        experiments = Experiment.objects.all().order_by('-name')
        serializer = ExperimentSerializer(experiments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_experiment_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'MINERvA'}
        self.client.post(EXPERIMENTS_URL, payload)
        exists = Experiment.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_experiment_invalid(self):
        """Test creating a new experiment with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(EXPERIMENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        