"""forms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from rest_framework.routers import DefaultRouter

from forms_app.views import FormViewSet, AnswerCreateAPIView, UserFormsAPIView

router = DefaultRouter()
router.register(r"forms", FormViewSet, basename="forms")

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path(
        "questions/<int:pk>/answer/",
        AnswerCreateAPIView.as_view(),
        name="answer-question",
    ),
    path("users/<int:pk>/forms/", UserFormsAPIView.as_view(), name="forms-question"),
    *router.urls,
]
