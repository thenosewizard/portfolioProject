# Generated by Django 2.1.5 on 2019-01-29 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0025_auto_20190129_1311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='schoolSup',
            new_name='schoolsup',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='travelDuration',
            new_name='travelTime',
        ),
    ]