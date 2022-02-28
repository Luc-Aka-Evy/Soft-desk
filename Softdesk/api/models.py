from django.db import models
from django.conf import settings

# Create your models here.
class Projects(models.Model):

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

class Issues(models.Model):

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project_id = models.IntegerField()
    status = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigne')
    created_time = models.DateTimeField(auto_now_add=True)
    

class Contributors(models.Model):

    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    class Meta:
        unique_together = ('user_id', 'project_id')


class Comments(models.Model):

    comment_id = models.IntegerField()
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    
