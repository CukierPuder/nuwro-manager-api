# Generated by Django 2.2.6 on 2019-12-15 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_artifact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultfile',
            name='related_datafiles',
        ),
        migrations.AddField(
            model_name='resultfile',
            name='z_axis',
            field=models.CharField(max_length=255, null=True),
        ),
    ]