# Generated by Django 4.0.2 on 2022-03-01 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_projects_project_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='comment_id',
        ),
    ]
