from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import *

app_name="user"

router = DefaultRouter()
router.register('user', AccountViewset,basename="account")

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/me/', UserRetiveUpdate.as_view(), name="me"),
    path('api/get-token/', TokenloginApiView.as_view(), name="token"),
]
