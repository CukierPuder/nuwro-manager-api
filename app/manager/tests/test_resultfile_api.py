import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.files import File

from rest_framework import status
from rest_framework.test import APIClient

from unittest.mock import MagicMock

from manager.serializers import (
    ResultfileListSerializer,
    ResultfileDetailSerializer
)
from core.models import (
    Experiment,
    Measurement,
    Nuwroversion,
    Resultfile
)


RESULTFILES_URL = reverse('manager:resultfile-list')


def generate_file_link(experiment_name,
                       measurement_name,
                       nuwroversion_name,
                       filename):
    """Generate filepath for new Resultfile file"""
    return os.path.join(
        (f'media/uploads/resultfiles'
         f'/{experiment_name}'
         f'/{measurement_name}'
         f'/{nuwroversion_name}'), filename)


def detail_url(resultfile_id):
    """Return a resultfile detail url"""
    return reverse('manager:resultfile-detail', args=[resultfile_id])


def sample_experiment(name='MINERvA'):
    """Create and return the sample experiment"""
    return Experiment.objects.create(name=name)


def sample_measurement(name='CC0pi'):
    """Create and return the sample measurement"""
    return Measurement.objects.create(name=name)


def sample_nuwroversion(name='v1.0'):
    """Create and return the sample nuwroversion"""
    return Nuwroversion.objects.create(name=name)


def sample_resultfile(filename='test.txt'):
    """Create and return sample Resultfile"""
    file_mock = MagicMock(spec=File)
    file_mock.name = filename

    defaults = {
        'experiment': sample_experiment(),
        'measurement': sample_measurement(),
        'nuwroversion': sample_nuwroversion(),
        'is_3d': False,
        'description': 'Test description',
        'x_axis': 'X AXIS NAME',
        'y_axis': 'Y AXIS NAME',
        'filename': file_mock.name,
        'result_file': file_mock
    }
    return Resultfile.objects.create(**defaults)


class PublicResultfileApiTests(TestCase):
    """Test unauthenticated resultfile API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RESULTFILES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateResultfileApiTests(TestCase):
    """Test authenticated resultfile API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_resultfiles(self):
        """Test retrieving a list of resultfiles"""
        sample_resultfile()

        res = self.client.get(RESULTFILES_URL)
        resultfiles = Resultfile.objects.all()
        serializer = ResultfileListSerializer(resultfiles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_resultfile(self):
        """Test creating resultfile"""
        experiment = sample_experiment()
        measurement = sample_measurement()
        nuwroversion = sample_nuwroversion()
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test_result.txt'

        payload = {
            'experiment': experiment.id,
            'measurement': measurement.id,
            'nuwroversion': nuwroversion.id,
            'is_3d': True,
            'description': 'Test description',
            'x_axis': 'X AXIS NAME',
            'y_axis': 'Y AXIS NAME',
            'filename': file_mock.name,
            'result_file': file_mock,
        }

        res = self.client.post(RESULTFILES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_file_exists_in_its_location(self):
        """Test the file exists in location provided by link field"""
        resultfile = sample_resultfile()
        self.assertTrue(os.path.exists(resultfile.result_file.path))

    def test_view_resultfile_detail(self):
        """Test viewing a resultfile detail"""
        resultfile = sample_resultfile()
        url = detail_url(resultfile.id)
        res = self.client.get(url)
        serializer = ResultfileDetailSerializer(resultfile)

        self.assertEqual(res.data, serializer.data)
