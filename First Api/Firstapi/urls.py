from django.urls import path, include
from Firstapi import views
urlpatterns = [
    path("hello/",views.HelloApiView.as_view()),
]
