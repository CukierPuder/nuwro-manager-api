# Generated by Django 2.2.3 on 2019-07-25 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_datafile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datafile',
            old_name='file_obj',
            new_name='input_file',
        ),
    ]
