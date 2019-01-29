# Generated by Django 2.1.5 on 2019-01-26 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_auto_20190126_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='quiz_assigned',
        ),
        migrations.AddField(
            model_name='question',
            name='quiz_assigned',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz'),
        ),
    ]