from django.urls import path,include
from . import views

app_name = "main"


urlpatterns = [
	path('',views.homepage,name="homepage"),
	path('register/',views.register,name="register"),
	path('logout/',views.logout_page,name="logout_page"),
	path('login/',views.login_page,name="login_page"),
	path('<single_slug>/',views.single_slug_handler,name="single_slug_handler")

]