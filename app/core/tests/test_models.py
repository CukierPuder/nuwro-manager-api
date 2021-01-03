from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files import File
from unittest.mock import MagicMock

from core import models


def sample_artifact(resultfile, filename='art1.txt'):
    """Create and return sample artifact file"""
    file_mock = MagicMock(spec=File)
    file_mock.name = filename

    defaults = {
        'resultfile': resultfile,
        'filename': file_mock.name,
        'artifact': file_mock
    }
    return models.Artifact.objects.create(**defaults)


def sample_resultfile(experiment='MINERvA',
                      measurement='CC0pi',
                      nuwroversion='v1.0',
                      filename='res.txt'):
    """Create and return sample resultfile"""
    file_mock = MagicMock(spec=File)
    file_mock.name = filename

    defaults = {
        'experiment': models.Experiment.objects.create(name=experiment),
        'measurement': models.Measurement.objects.create(name=measurement),
        'nuwroversion': models.Nuwroversion.objects.create(name=nuwroversion),
        'is_3d': False,
        'description': 'Some random description',
        'filename': file_mock.name,
        'result_file': file_mock
    }
    return models.Resultfile.objects.create(**defaults)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EXamPLE.cOm'
        user = get_user_model().objects.create_user(
            email=email,
            password='password123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            # anything running here should raise the ValueError
            get_user_model().objects.create_user(None, 'password123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='password123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_experiment_str(self):
        """Test the experiment string representation"""
        experiment = models.Experiment.objects.create(
            name='MINERvA'
        )
        self.assertEqual(str(experiment), experiment.name)

    def test_measurement_str(self):
        """Test the measurement string representation"""
        measurement = models.Measurement.objects.create(
            name='CC0pi'
        )
        self.assertEqual(str(measurement), measurement.name)

    def test_nuwroversion_str(self):
        """Test the nuwroversion string representation"""
        nuwroversion = models.Nuwroversion.objects.create(
            name='v1.0'
        )
        self.assertEqual(str(nuwroversion), nuwroversion.name)

    def test_artifact_str(self):
        """Test the Artifact string representation"""
        tmp_resultfile = sample_resultfile()
        file_mock = MagicMock(spec=File)
        file_mock.name = 'artifact_file.txt'

        artifact = sample_artifact(
            resultfile=tmp_resultfile,
            filename=file_mock.name
        )
        self.assertEqual(str(artifact), artifact.filename.split('/')[-1])

    def test_resultfile_str(self):
        """Test the Resultfile string representation"""
        experiment = models.Experiment.objects.create(name='MINERvA')
        measurement = models.Measurement.objects.create(name='CC0pi')
        nuwroversion = models.Nuwroversion.objects.create(name='v1.0')
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test.txt'

        resultfile = models.Resultfile.objects.create(
            experiment=experiment,
            measurement=measurement,
            nuwroversion=nuwroversion,
            is_3d=False,
            description='Test description',
            result_file=file_mock,
        )

        self.assertEqual(
            str(resultfile),
            resultfile.result_file.name.split('/')[-1]
        )
