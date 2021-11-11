"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from projects.views import ProjectsViewSet, UsersViewSet, IssuesViewSet, CommentsViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'projects', ProjectsViewSet, basename='projects')
projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'users', UsersViewSet, basename='project-users')
projects_router.register(r'issues', IssuesViewSet, basename='project-issues')
issues_routers = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issue')
issues_routers .register(r'comments', CommentsViewSet, basename='project-issues-comments')

urlpatterns = [
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_routers .urls))

]
