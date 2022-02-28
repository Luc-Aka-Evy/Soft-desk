from urllib import request
from xml.etree.ElementInclude import include
from rest_framework import serializers
from api.models import Projects, Contributors, Issues, Comments
from authentication.models import User
from authentication.serializers import UserSerializer

        
class ProjectsSerializer(serializers.ModelSerializer):
    
   
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

    
    def validate_title(self, value):
        if Projects.objects.filter(title=value).exists():
            raise serializers.ValidationError('Title already exists')
        return value

    def validate_description(self, value):
        if Projects.objects.filter(description=value).exists():
            raise serializers.ValidationError('There is a project with the same description please change it')
        return value
    

class ContributorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user_id', 'project_id', 'permission', 'role']


class IssuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issues
        fields = ['project_id', 'title', 'description', 'tag', 'priority', 'status', 'author_user_id', 'assignee_user_id', 'created_time']


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['comment_id', 'description', 'author_user_id', 'issue_id', 'created_time']