# Generated by Django 2.2.3 on 2019-07-23 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_measurement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nuwroversion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]