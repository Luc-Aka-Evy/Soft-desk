from django.db import models
from django.conf import settings

# Create your models here.
class Projects(models.Model):

    project_id = models.IntegerField()
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributors', related_name='contributions')


class Issues(models.Model):

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project_id = models.IntegerField()
    status = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    


class Contributors(models.Model):

    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.Choices()
    role = models.CharField(max_length=128)


class Comments(models.Model):

    comment_id = models.IntegerField()
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    
