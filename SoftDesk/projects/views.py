from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from django.views.generic.detail import SingleObjectMixin
from rest_framework import mixins, status
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectsListSerializer, ProjectDetailSerializer, ContributorsListSerializer
from .serializers import IssueDetailSerializer, ContributorDetailSerializer, IssuesListSerializer
from .serializers import CommentDetailSerializer, CommentsListSerializer
from users.models import User
from .permissions import IsOwnerProjectOrReadOnly, IsOwnerIssueOrCommentOrReadOnly


class MultipleSerializerMixin:
    """ Return the detail serializer when action is retrieve """

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectsViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    Provides the list of user's projects list and access to the details
    of a specific project.
    From the detailed view user can update or delete a project of the list
    if is the actual author of the author
    """

    permission_classes = [IsOwnerProjectOrReadOnly]

    serializer_class = ProjectsListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        """ Return the list of projects to which the user contributes """
        queryset = Project.objects.all()
        contributor = self.request.user
        if contributor:
            queryset = queryset.filter(contributors=contributor)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Override create function to set the logged in user as the
        author of the project when a new project is create and create a
        contributor instance for this project with the user's data
        """

        serializer= ProjectDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author_id=self.request.user.id)

        headers = self.get_success_headers(serializer.data)
        project = Project.objects.create(title=request.data['title'],
                         description=request.data['description'],
                         type=request.data['type'],
                         author_id=self.request.user.id)

        contributor = Contributor.objects.create(project=project,
                                                 user=self.request.user,
                                                 permission='YES',
                                                 role='AUTHOR')
        contributor.save()
        serializer_contributor = ContributorDetailSerializer(contributor)
        return Response(serializer_contributor.data, status=status.HTTP_201_CREATED, headers=headers)


class UsersViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    Provides the list of contributor's for a specific project and give
    access to a specific contributor detailed view.
    From the detailed view user can update or delete a contributor of the list
    """

    serializer_class = ContributorsListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        """ Return the list of contributors associated to a specific project """
        return Contributor.objects.filter(project=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        """
        Override create function to set the specific project as contributor
        attribute project and the contributor attribute user as the instance
        user with the id passed
        """
        serializer = ContributorDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.filter(id=self.kwargs['project_pk']).first()
        user_id = request.data['user_id']
        user = User.objects.filter(id=user_id).first()
        serializer.save(user=user, project=project)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IssuesViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    Provides the list of issue's for a specific project and give access to a
    specific issue detailed view. The detailed view allowed user to update or
    delete an issue of the list if he is the author of this issue
    """

    permission_classes = [IsOwnerIssueOrCommentOrReadOnly]

    serializer_class = IssuesListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        """ Return the list of issues associated to a specific project """
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        """
        Override create function to set all contributors of the project as
        assigned_user and the logged in user as the author
        """

        project = Project.objects.filter(id=self.kwargs['project_pk']).first()
        user = User.objects.filter(id=project.author_id).first()
        author = Contributor.objects.filter(user=user).first()
        serializer = IssueDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author_user=self.request.user,assigned_user=author, project_id=project.id)


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentsViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    Provides the list of comment's for a specific issue and give access to a
    specific comment detailed view. The detailed view allowed user to update or
    delete a comment of the list if he is the author of this comment.
    """

    permission_classes = [IsOwnerIssueOrCommentOrReadOnly]

    serializer_class = CommentsListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        """ Return the list of comments linked to a specific issue """
        issue = Issue.objects.filter(pk=self.kwargs['issue_pk']).first()
        comments = Comment.objects.filter(issue=issue)
        return comments

    def create(self, request, *args, **kwargs):
        """
        Override create function to set comment attribute issue as the
        specific issue he is looking and the logged in user as the author
        """
        serializer = CommentDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        issue = Issue.objects.filter(pk=self.kwargs['issue_pk']).first()
        serializer.save(author_user=self.request.user, issue=issue)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


