# Generated by Django 2.1.5 on 2019-01-29 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0026_auto_20190129_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='identify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_needed', models.CharField(blank=True, choices=[('yes', 'yes'), ('no', 'no')], max_length=50)),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Student')),
            ],
        ),
    ]
