
import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core.files import File

from rest_framework import status
from rest_framework.test import APIClient

from unittest.mock import MagicMock

from core.tests.test_models import sample_resultfile, sample_artifact
from core.models import Artifact
from manager.serializers import ArtifactSerializer, ArtifactDetailSerializer


ARTIFACTS_URL = reverse('manager:artifact-list')


def generate_file_link(experiment_name,
                       measurement_name,
                       nuwroversion_name,
                       resultfile_name,
                       artifact_name):
    """Generate filepath for new artifact file"""
    return os.path.join(
        f'media/uploads/artifacts/{experiment_name}/{measurement_name}/{nuwroversion_name}/{resultfile_name.split(".")[0]}/',
        artifact_name
    )


def detail_url(artifact_id):
    """Return artifact detail url"""
    return reverse('manager:artifact-detail', args=[artifact_id])


class PublicArtifactApiTests(TestCase):
    """Test unauthenticated access to Artifact API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(ARTIFACTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateArtifactApiTests(TestCase):
    """Test authorized access to Artifact API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_all_artifacts(self):
        """Test retrieving a list of all existing Artifacts"""
        resfile = sample_resultfile()
        resfile2 = sample_resultfile(
            experiment='MINERvB',
            measurement='CC0',
            nuwroversion='v1.1',
            filename='art2.txt'
        )

        sample_artifact(resultfile=resfile, filename='art1.txt')
        sample_artifact(resultfile=resfile, filename='art2.txt')
        sample_artifact(resultfile=resfile2, filename='art3.txt')
        sample_artifact(resultfile=resfile2, filename='art4.txt')

        res = self.client.get(ARTIFACTS_URL)
        artifacts = Artifact.objects.all()
        serializer = ArtifactSerializer(artifacts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_artifacts_for_particular_resultfile(self):
        """Test retrieving a list of artifacts related to particular Resultfile"""
        resfile = sample_resultfile()
        resfile2 = sample_resultfile(
            experiment='MINERvB',
            measurement='CC0',
            nuwroversion='v1.1',
            filename='art2.txt'
        )

        sample_artifact(resultfile=resfile, filename='art1.txt')
        sample_artifact(resultfile=resfile, filename='art2.txt')
        sample_artifact(resultfile=resfile2, filename='art3.txt')
        sample_artifact(resultfile=resfile2, filename='art4.txt')

        res = self.client.get(ARTIFACTS_URL, {'resultfile': resfile.id})
        artifacts = Artifact.objects.filter(resultfile=resfile)
        serializer = ArtifactSerializer(artifacts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_artifact(self):
        """Test creating Artifact"""
        tmp_resfile = sample_resultfile()
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test_art1.txt'

        payload = {
            'resultfile': tmp_resfile.id,
            'filename': file_mock.name,
            'artifact': file_mock
        }

        res = self.client.post(ARTIFACTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tmp_resfile.id, res.data['resultfile'])

    def test_file_exists_in_its_location(self):
        """Test the newly created file exists in location provided by link field"""
        tmp_resultfile = sample_resultfile()
        artifact = sample_artifact(tmp_resultfile)
        self.assertTrue(os.path.exists(artifact.artifact.path))

    def test_artifact_detail_view(self):
        """Test viewing an Artifact detail"""
        artifact = sample_artifact(sample_resultfile())
        url = detail_url(artifact_id=artifact.id)
        res = self.client.get(url)
        serializer = ArtifactDetailSerializer(artifact)

        self.assertEqual(res.data, serializer.data)
