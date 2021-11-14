from .models import Project, Contributor, Issue, Comment
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Serialize user without details - used in the :
    - ProjectDetailSerializer
    - AssignedUserSerializer
    - IssueDetailSerializer
    - CommentDetailSerializer
    """

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class DetailUserSerializer(serializers.ModelSerializer):
    """ Serialize detailed user - used in the """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProjectsListSerializer(serializers.ModelSerializer):
    """ Serialize a list of projects - used in the view """

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']


class ProjectDetailSerializer(serializers.ModelSerializer):
    """ Serialize details about a specific project - used in the view """

    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type',
                  'contributors']

    def get_contributors(self, instance):
        queryset = instance.contributors.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data


class ProjectContributorSerializer(serializers.ModelSerializer):
    """
    Serialize a project id and title - used in :
    - ContributorsListSerializer
    - ContributorDetailSerializer
    - IssuesListSerializer
    """

    class Meta:
        model = Project
        fields = ['id', 'title']


class ContributorsListSerializer(serializers.ModelSerializer):
    """
    Serialize a list of contributors for a specific  project - used in the view
    """

    project = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['id', 'project', 'user', 'permission', 'role']

    def get_project(self, instance):
        queryset = instance.project
        serializer = ProjectContributorSerializer(queryset, many=False)
        return serializer.data


class ContributorDetailSerializer(serializers.ModelSerializer):
    """ Serialize details about a specific contributor - used in the view """

    user = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['project', 'user', 'permission', 'role']

    def get_user(self, instance):
        user = instance.user
        serializer = DetailUserSerializer(user, many=False)
        return serializer.data

    def get_project(self, instance):
        queryset = instance.project
        serializer = ProjectContributorSerializer(queryset, many=False)
        return serializer.data


class IssuesListSerializer(serializers.ModelSerializer):
    """
    Serialize a list of issues for a specific project - used in the view
    """

    project = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['project', 'id', 'title', 'description', 'tag', 'priority', 'status']

    def get_project(self, instance):
        queryset = Project.objects.filter(id=instance.project_id).first()
        serializer = ProjectContributorSerializer(queryset, many=False)
        return serializer.data


class AssignedUserSerializer(serializers.ModelSerializer):
    """
    Serialize contributor name and role - used in :
    - IssueDetailSerializer
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['name', 'role']

    def get_name(self, instance):
        name = instance.user
        serializer = UserSerializer(name, many=False)
        return serializer.data


class IssueDetailSerializer(serializers.ModelSerializer):
    """ Serialize details about a specific issue - used in the view """

    author_user = serializers.SerializerMethodField()
    assigned_user = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status',
                  'author_user', 'assigned_user']

    def get_author_user(self, instance):
        queryset = instance.author_user
        serializer = UserSerializer(queryset, many=False)
        return serializer.data

    def get_assigned_user(self, instance):
        queryset = instance.assigned_user
        serializer = AssignedUserSerializer(queryset, many=True)
        return serializer.data


class IssueCommentDetailSerializer(serializers.ModelSerializer):
    """
    Serialize issue id, title and description - used in :
    - CommentsListSerializer
    - CommentDetailSerializer
    """

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description']


class CommentsListSerializer(serializers.ModelSerializer):
    """
    Serialize a list of comments for a specific issue - used in the view
    """

    issue = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['issue', 'id', 'description', 'created_time']

    def get_issue(self, instance):
        queryset = instance.issue
        serializer = IssueCommentDetailSerializer(queryset, many=False)
        return serializer.data


class CommentDetailSerializer(serializers.ModelSerializer):
    """ Serialize details about a specific comment - used in the view """

    author_user = serializers.SerializerMethodField()
    issue = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user', 'issue', 'created_time']

    def get_author_user(self, instance):
        queryset = instance.author_user
        serializer = UserSerializer(queryset, many=False)
        return serializer.data

    def get_issue(self, instance):
        queryset = instance.issue
        serializer = IssueCommentDetailSerializer(queryset, many=False)
        return serializer.data