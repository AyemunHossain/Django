from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()

router.register('courses', CourseViewset, basename="courses")
router.register('review',ReviewViewset, basename="review")

urlpatterns = [
	path('auth-api/', include('rest_framework.urls', namespace="rest_framework")),
	path('api/list/', ListCourseView.as_view(), name="listCourse"),
	path('api/<int:pk>/', RetrieveUpdateDestoryCourse.as_view(), name="RUDcourses"),
	path('api/<int:course_id>/review/',ListReviewView.as_view(), name="listReview"),
	# path('api/<int:course_id>/review/<int:pk>/',RetrieveUpdateDestoryReview.as_view(), name="RUDreview"),

	path('api/viewsets/',include(router.urls,))
]
