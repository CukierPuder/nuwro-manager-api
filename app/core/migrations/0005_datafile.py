# Generated by Django 2.2.3 on 2019-07-25 09:51

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_nuwroversion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Datafile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable', models.CharField(blank=True, max_length=255)),
                ('x_axis', models.CharField(max_length=255)),
                ('y_axis', models.CharField(max_length=255)),
                ('file_obj', models.FileField(unique=True, upload_to=core.models.datafile_file_path)),
                ('link', models.CharField(max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Experiment')),
                ('measurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Measurement')),
            ],
        ),
    ]
