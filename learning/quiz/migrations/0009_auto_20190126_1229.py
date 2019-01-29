# Generated by Django 2.1.5 on 2019-01-26 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_auto_20190126_1144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='summary',
            options={'verbose_name': 'Finished_quiz', 'verbose_name_plural': 'Finished_quizzes'},
        ),
        migrations.RenameField(
            model_name='questionpost',
            old_name='finished_quizzes',
            new_name='record',
        ),
        migrations.RemoveField(
            model_name='questionpost',
            name='quiz',
        ),
        migrations.AddField(
            model_name='summary',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz'),
        ),
    ]