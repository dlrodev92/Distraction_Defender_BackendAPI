# Generated by Django 3.2.21 on 2024-04-05 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_project_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='projectImages/', verbose_name='image'),
        ),
    ]
