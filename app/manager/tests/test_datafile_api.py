
import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.files import File

from rest_framework import status
from rest_framework.test import APIClient

from unittest.mock import MagicMock

from core.models import Datafile, Experiment, Measurement
from manager.serializers import (
    DatafileListSerializer,
    DatafileDetailSerializer
)


DATAFILES_URL = reverse('manager:datafile-list')


def generate_file_link(experiment_name, measurement_name, filename):
    """Generate filepath for new Datafile file"""

    return os.path.join(
        f'media/uploads/datafiles/{experiment_name}/{measurement_name}/',
        filename
    )


def detail_url(datafile_id):
    """Return datafile detail url"""
    return reverse('manager:datafile-detail', args=[datafile_id])


def sample_experiment(name='MINERvA'):
    """Create and return the sample experiment"""
    return Experiment.objects.create(name=name)


def sample_measurement(name='CC0pi'):
    """Create and return the sample measurement"""
    return Measurement.objects.create(name=name)


def sample_datafile(
    filename='test.txt',
    experiment='MINERvA',
    measurement='CC0pi'
):
    """Create and return sample datafile"""
    file_mock = MagicMock(spec=File)
    file_mock.name = filename

    defaults = {
        'experiment': sample_experiment(experiment),
        'measurement': sample_measurement(measurement),
        'variable': 'test variable',
        'filename': file_mock.name,
        'input_file': file_mock
    }
    return Datafile.objects.create(**defaults)


class PublicDatafileApiTests(TestCase):
    """Test unauthenticated datafile API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(DATAFILES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDatafileApiTests(TestCase):
    """Test authenticated datafile API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_datafiles(self):
        """Test retrieving a list of datafiles"""
        sample_datafile()
        sample_datafile()

        res = self.client.get(DATAFILES_URL)
        datafiles = Datafile.objects.all()
        serializer = DatafileListSerializer(datafiles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_datafile(self):
        """Test creating datafile"""
        experiment = sample_experiment()
        measurement = sample_measurement()

        file_mock = MagicMock(spec=File)
        file_mock.name = 'test.txt'

        payload = {
            'experiment': experiment.id,
            'measurement': measurement.id,
            'variable': 'Test variable',
            'filename': file_mock.name,
            'input_file': file_mock
        }

        res = self.client.post(DATAFILES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(experiment.id, res.data['experiment'])
        self.assertEqual(measurement.id, res.data['measurement'])
        generated_file_link = generate_file_link(experiment.name,
                                                 measurement.name,
                                                 file_mock.name)
        self.assertEqual(generated_file_link, res.data['link'])

    def test_file_exists_in_its_location(self):
        """Test the file exists in location provided by link field"""
        datafile = sample_datafile()
        self.assertTrue(os.path.exists(f'/vol/web/{datafile.link}'))

    def test_view_datafile_detail(self):
        """Test viewing a datafile detail"""
        datafile = sample_datafile()
        url = detail_url(datafile.id)
        res = self.client.get(url)
        serializer = DatafileDetailSerializer(datafile)

        self.assertEqual(res.data, serializer.data)

    def test_filter_datafile_by_experiment_and_measurement(self):
        """Test returning datafiles filtered by experiment and measurement"""
        datafile1 = sample_datafile(
            filename='ashery.txt',
            experiment='MINERvA',
            measurement='CC0pi'
        )
        datafile2 = sample_datafile(
            filename='navon.txt',
            experiment='MINERvA',
            measurement='CC0pi'
        )
        datafile3 = sample_datafile(
            filename='ashon.txt',
            experiment='MINERvB',
            measurement='CC0'
        )

        res = self.client.get(
            DATAFILES_URL,
            {
                'experiment': f'{datafile1.experiment.id}',
                'measurement': f'{datafile1.measurement.id}'
            }
        )

        ser1 = DatafileListSerializer(datafile1)
        ser2 = DatafileListSerializer(datafile2)
        ser3 = DatafileListSerializer(datafile3)

        self.assertIn(ser1.data, res.data)
        self.assertIn(ser2.data, res.data)
        self.assertNotIn(ser3.data, res.data)
