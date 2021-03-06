# Generated by Django 2.1.5 on 2019-01-27 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0014_auto_20190127_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='machineLearn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(max_length=50)),
                ('age', models.IntegerField(default=0)),
                ('travelTime', models.IntegerField(default=0)),
                ('studytime', models.IntegerField(default=0)),
                ('failures', models.IntegerField(default=0)),
                ('schoolsup', models.CharField(max_length=3)),
                ('activities', models.CharField(max_length=3)),
                ('higher', models.CharField(max_length=3)),
                ('freetime', models.IntegerField(default=0)),
                ('absences', models.IntegerField(default=0)),
                ('passed', models.CharField(max_length=3)),
            ],
        ),
    ]
