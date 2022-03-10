# Generated by Django 4.0.2 on 2022-03-07 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_alter_issues_project_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comments",
            old_name="author_user_id",
            new_name="author",
        ),
        migrations.RenameField(
            model_name="comments",
            old_name="issue_id",
            new_name="issue",
        ),
        migrations.RenameField(
            model_name="contributors",
            old_name="project_id",
            new_name="project",
        ),
        migrations.RenameField(
            model_name="contributors",
            old_name="user_id",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="issues",
            old_name="assignee_user_id",
            new_name="assignee",
        ),
        migrations.RenameField(
            model_name="issues",
            old_name="author_user_id",
            new_name="author",
        ),
        migrations.RenameField(
            model_name="issues",
            old_name="project_id",
            new_name="project",
        ),
        migrations.RenameField(
            model_name="projects",
            old_name="author_user_id",
            new_name="author",
        ),
    ]