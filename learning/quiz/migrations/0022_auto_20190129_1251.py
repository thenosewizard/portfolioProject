# Generated by Django 2.1.5 on 2019-01-29 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0021_auto_20190128_2350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='cca',
            new_name='activities',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='gender',
            new_name='sex',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='absence',
            new_name='studytime',
        ),
        migrations.RemoveField(
            model_name='student',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='student',
            name='siteTimeDuration',
        ),
        migrations.AddField(
            model_name='student',
            name='absences',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='freetime',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='higher',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]
