# Generated by Django 2.1.5 on 2019-01-11 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quiz_topic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finished_quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Finished_quiz',
                'verbose_name_plural': 'Finished_quizs',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.AlterField(
            model_name='question',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.subTopic'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.Subject'),
        ),
        migrations.AddField(
            model_name='student',
            name='assigned_quizzes',
            field=models.ManyToManyField(to='quiz.Quiz'),
        ),
    ]