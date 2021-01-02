import os

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from uuid import uuid4


def datafile_file_path(instance, filename):
    """Generate filepath for new Datafile file"""
    ext = filename.split('.')[-1]
    uuid = str(uuid4()).replace('-', '')

    return os.path.join(
        (f'uploads/datafiles/'
         f'{instance.experiment.name}'
         f'/{instance.measurement.name}/'),
        '.'.join([uuid, ext])
    )


def artifact_file_path(instance, filename):
    """Generate filepath for new Artifact file"""
    ext = filename.split('.')[-1]
    uuid = str(uuid4()).replace('-', '')

    return os.path.join(
        (f'uploads/artifacts'
         f'/{instance.experiment.name}'
         f'/{instance.measurement.name}'
         f'/{instance.filename.split(".")[0]}'),
        '.'.join([uuid, ext])
        )


def resultfile_file_path(instance, filename):
    """Generate filepath for a new Resultfile file"""
    ext = filename.split('.')[-1]
    uuid = str(uuid4()).replace('-', '')

    return os.path.join(
        (f'uploads/resultfiles/'
         f'{instance.experiment.name}'
         f'/{instance.measurement.name}'
         f'/{instance.nuwroversion.name}'),
        '.'.join([uuid, ext])
    )


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Experiment(models.Model):
    """Experiment to be used for a ResultFile"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    """Measurement to be used for a ResultFile"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Nuwroversion(models.Model):
    """Nuwroversion to be used for a ResultFile"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Resultfile(models.Model):
    """Respresents the nuwro result text file"""
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    nuwroversion = models.ForeignKey(Nuwroversion, on_delete=models.CASCADE)
    is_3d = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    x_axis = models.CharField(max_length=255, blank=False)
    y_axis = models.CharField(max_length=255, blank=False)
    z_axis = models.CharField(max_length=255, null=True)
    filename = models.CharField(max_length=255)
    result_file = models.FileField(
        unique=True,
        null=False,
        upload_to=resultfile_file_path
    )
    link = models.CharField(max_length=255, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.filename:
            return self.filename
        return self.result_file.name.split('/')[-1]
    
    class Meta:
        ordering = ['-creation_date']


class Artifact(models.Model):
    filename = models.CharField(max_length=255, blank=False)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    artifact = models.FileField(null=False, upload_to=artifact_file_path, blank=False)
    link = models.CharField(max_length=255, null=True)
    addition_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.filename:
            return self.filename
        return self.file.name.split('/')[-1]
    
    class Meta:
        ordering = ['-addition_date']
