
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import UserPublicProfile

app_name = "users"

urlpatterns=[
	path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),
												name='userLogin'),

	path('logout/',views.userLogout,name='userLogout'),
	path('signup/',views.userSignup,name='userSignup'),
	path('profile/',views.userProfile,name='userProfile'),
	path('profiles/<str:username>',UserPublicProfile.as_view(),
									name='userPublicProfile'),

	path('profile/update/',views.userProfileUpdate,name='userProfileUpdate'),

]

