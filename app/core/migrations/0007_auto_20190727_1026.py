# Generated by Django 2.2.3 on 2019-07-27 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190725_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='filename',
            field=models.CharField(default='test.txt', max_length=255),
        ),
        migrations.AlterField(
            model_name='datafile',
            name='link',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
