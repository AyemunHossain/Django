from django.urls import path
from django.contrib.auth.decorators import login_required
from .import views
from .views import (PostDetailView,
	PostCreateView,PostUpdateView,PostDeleteView,
	UserPostsListView )

app_name = "blogPosts"

urlpatterns = [
	path('',views.homePage,name="homePage"),
	path('posts/<str:username>/',UserPostsListView.as_view(),name="userPostsPage"),
	path('post/<int:pk>/',PostDetailView.as_view(),name="postDetail"),
	path('post/create/',login_required(PostCreateView.as_view()),name="postCreate"),
	path('post/<int:pk>/update/',login_required(PostUpdateView.as_view()),name="postUpdate"),
	path('post/<int:pk>/delete/',login_required(PostDeleteView.as_view()),name="postDelete"),
]