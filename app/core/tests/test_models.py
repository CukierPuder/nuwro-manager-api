from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


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
