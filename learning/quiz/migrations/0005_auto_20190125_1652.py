# Generated by Django 2.1.5 on 2019-01-25 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_remove_questionpost_quiz_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionpost',
            name='questionDone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Question'),
        ),
        migrations.AddField(
            model_name='questionpost',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz'),
        ),
    ]
