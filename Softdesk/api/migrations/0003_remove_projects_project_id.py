# Generated by Django 4.0.2 on 2022-02-27 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='project_id',
        ),
    ]
