from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Nuwroversion
from manager.serializers import NuwroversionSerializer


NUWROVERIONS_URL = reverse('manager:nuwroversion-list')


def detail_url(nuwroversion_id):
    """Return nuwroversion detail url"""
    return reverse('manager:nuwroversion-detail', args=[nuwroversion_id])


class PublicNuwroversionApiTests(TestCase):
    """Test publicly available nuwroversion API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving nuwroversions"""
        res = self.client.get(NUWROVERIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNuwroversionApiTest(TestCase):
    """Test the authorized user nuwroversion API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_nuwroversions(self):
        """Test retrieving nuwroversions"""
        Nuwroversion.objects.create(name='v1.0')
        Nuwroversion.objects.create(name='v2.0')

        res = self.client.get(NUWROVERIONS_URL)
        nuwroversions = Nuwroversion.objects.all().order_by('-name')
        serializer = NuwroversionSerializer(nuwroversions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_nuwroversions_successful(self):
        """Test creating new nuwroversion"""
        payload = {'name': 'v1.0'}
        self.client.post(NUWROVERIONS_URL, payload)
        exists = Nuwroversion.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_invalid_nuwroversion(self):
        """Test creating a new nuwroversion with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(NUWROVERIONS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_particular_nuwroversion(self):
        """Test patching an existing nuwroversion"""
        Nuwroversion.objects.create(name='CC0px')
        Nuwroversion.objects.create(name='CC0')
        nuwroversion_to_patch = Nuwroversion.objects.get(name='CC0px')
        url = detail_url(nuwroversion_to_patch.id)
        payload = {'name': 'XX0pc'}
        res = self.client.patch(url, payload)
        exists = Nuwroversion.objects.filter(name=payload['name']).exists()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(exists)
