# Generated by Django 2.1.5 on 2019-01-27 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0016_auto_20190127_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinelearn',
            name='travelTime',
            field=models.IntegerField(default=1),
        ),
    ]
