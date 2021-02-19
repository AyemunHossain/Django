from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("user.urls")),
    path('auth-api/',include('rest_framework.urls',namespace="rest_framework")),
]
