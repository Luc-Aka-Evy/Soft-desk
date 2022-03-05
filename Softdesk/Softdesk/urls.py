"""Softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from posixpath import basename
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import (
    ProjectsViewset,
    ContributorsViewset,
    IssuesViewset,
    CommentsViewset,
)
from authentication.views import UserViewset, UserCreate

router = routers.SimpleRouter()

router.register("projects", ProjectsViewset, basename="projects")
router.register("users", UserViewset, basename="users")
router.register("issues", IssuesViewset, basename="issues")

projects_router = routers.NestedSimpleRouter(router, "projects", lookup="projects")
projects_router.register("users", ContributorsViewset, basename="contributors")
projects_router.register("issues", IssuesViewset, basename="issues-comments")

issues_router = routers.NestedSimpleRouter(projects_router, "issues", lookup="issues")
issues_router.register("comments", CommentsViewset, basename="comments")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path("api/", include(projects_router.urls)),
    path("api/", include(issues_router.urls)),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/signup/", UserCreate.as_view(), name="signup"),
]
