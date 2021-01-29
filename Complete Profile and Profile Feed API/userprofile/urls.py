from django.urls import path, include
from rest_framework.routers import DefaultRouter
from userprofile import views

router = DefaultRouter()
router.register('profile',views.UserProfileViewSet)
router.register('profile-feed',views.UserProfileFeedItemViewSet)

urlpatterns = [
	path('api/',include(router.urls)),
	path('api/login', views.UserLoginApiView.as_view()),
]
