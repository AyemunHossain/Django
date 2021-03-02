
from django.urls import path
from . import views

from .views import UserPublicProfile

app_name = "users"

urlpatterns=[
	path('login/', views.login_page, name='userLogin'),

	path('logout/',views.userLogout,name='userLogout'),
	path('signup/',views.userSignup,name='userSignup'),
	path('profile/',views.userProfile,name='userProfile'),
	path('profiles/<str:username>',UserPublicProfile.as_view(),
									name='userPublicProfile'),
	path('profile/update/',views.userProfileUpdate,name='userProfileUpdate'),

]

