from xml.etree.ElementInclude import include
from rest_framework import serializers
from api.models import Projects, Contributors, Issues, Comments
from authentication.models import User
from authentication.serializers import UserSerializer


class ProjectsSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Projects
        fields = ["id", "title", "description", "type", "author"]

    def save(self, **kwargs):
        """Include default for read_only `user` field"""
        kwargs["author"] = self.fields["author"].get_default()
        return super().save(**kwargs)

    def validate_title(self, value):
        if Projects.objects.filter(title=value).exists():
            raise serializers.ValidationError("Title already exists")
        return value


class ProjectsDetailSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ["id", "title", "description", "type", "author"]

    def get_author(self, instance):
        queryset = instance.author
        serializer = UserSerializer(queryset)
        return serializer.data


class ContributorsSerializer(serializers.ModelSerializer):

    user = serializers.CharField(write_only=True)

    class Meta:
        model = Contributors
        fields = ["id", "user", "role"]
        include = ["project"]

    def create(self, validated_data):
        project = Projects.objects.get(pk=self.context["view"].kwargs["projects_pk"])
        validated_data["project"] = project
        return Contributors.objects.create(**validated_data)

    def validate_user(self, value):
        project = Projects.objects.get(pk=self.context["view"].kwargs["projects_pk"])
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("There is no user with this username")

        if Contributors.objects.filter(
            user=User.objects.get(username=value), project=project
        ).exists():
            raise serializers.ValidationError("This user is a contributor already.")

        if User.objects.filter(username=value).exists():
            return User.objects.get(username=value)


class ContributorsDetailSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    class Meta:
        model = Contributors
        fields = ["id", "user", "role", "project"]

    def get_user(self, instance):
        queryset = instance.user
        serializer = UserSerializer(queryset)
        return serializer.data

    def get_project(self, instance):
        queryset = instance.project
        serializer = ProjectsSerializer(queryset)
        return serializer.data


class IssuesSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    assignee = serializers.CharField(write_only=True)

    class Meta:
        model = Issues
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "author",
            "assignee",
            "created_time",
        ]
        include = ["project"]

    def create(self, validated_data):
        project = Projects.objects.get(pk=self.context["view"].kwargs["projects_pk"])
        validated_data["project"] = project
        return Issues.objects.create(**validated_data)

    def save(self, **kwargs):
        """Include default for read_only `user` field"""
        kwargs["author"] = self.fields["author"].get_default()
        return super().save(**kwargs)

    def validate_title(self, value):
        project = Projects.objects.get(pk=self.context["view"].kwargs["projects_pk"])
        if Issues.objects.filter(title=value, project=project).exists():
            raise serializers.ValidationError(
                "An issue with this title already exists for this project"
            )
        return value

    def validate_assignee(self, value):
        project = Projects.objects.get(pk=self.context["view"].kwargs["projects_pk"])
        if not Contributors.objects.filter(
            user=User.objects.get(username=value), project=project
        ).exists():
            raise serializers.ValidationError(
                "This user is not a contributor of this project (change or add user in the contributors)."
            )

        if User.objects.filter(username=value).exists():
            return User.objects.get(username=value)


class IssuesDetailSerializer(serializers.ModelSerializer):

    project = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    assignee = serializers.SerializerMethodField()

    class Meta:
        model = Issues
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "project",
            "status",
            "author",
            "assignee",
            "created_time",
        ]

    def get_project(self, instance):
        queryset = instance.project
        serializer = ProjectsSerializer(queryset)
        return serializer.data

    def get_author(self, instance):
        queryset = instance.author
        serializer = UserSerializer(queryset)
        return serializer.data

    def get_assignee(self, instance):
        queryset = instance.assignee
        serializer = UserSerializer(queryset)
        return serializer.data


class CommentsSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        issue = Issues.objects.get(pk=self.context["view"].kwargs["issues_pk"])
        validated_data["issue"] = issue
        return Comments.objects.create(**validated_data)

    class Meta:
        model = Comments
        fields = ["id", "description", "author", "created_time"]
        include = ["issue"]

    def save(self, **kwargs):
        """Include default for read_only `user` field"""
        kwargs["author"] = self.fields["author"].get_default()
        return super().save(**kwargs)


class CommentsDetailSerializer(serializers.ModelSerializer):

    issue = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ["id", "description", "author", "issue", "created_time"]

    def get_author(self, instance):
        queryset = instance.author
        serializer = UserSerializer(queryset)
        return serializer.data

    def get_issue(self, instance):
        queryset = instance.issue
        serializer = IssuesSerializer(queryset)
        return serializer.data
