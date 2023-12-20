# Generated by Django 3.2.21 on 2023-12-20 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        ('projects', '0004_project_tasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tasks',
            field=models.ManyToManyField(blank=True, null=True, related_name='projects', to='tasks.Task'),
        ),
    ]
