from django.urls import path, include
from Firstapi import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello',views.HelloViewSet, basename ="hello-viewset")


urlpatterns = [
    path("hello/",views.HelloApiView.as_view()),
    path("viewset/",include(router.urls)),
]
