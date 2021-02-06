from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from courses.models import Review,Courses
from . import serializers
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from courses.customClass import ReviewCustomPagination

class ListCourseView(generics.ListCreateAPIView):
	queryset = Courses.objects.all()
	serializer_class = serializers.CoursesSerializer


class RetrieveUpdateDestoryCourse(generics.RetrieveUpdateDestroyAPIView):
	queryset = Courses.objects.all()
	serializer_class = serializers.CoursesSerializer
	permission_classes = (IsAuthenticatedOrReadOnly,)

class ListReviewView(generics.ListCreateAPIView):
	queryset = Review.objects.all()
	serializer_class = serializers.ReviewSerializer
	permission_classes = (IsAuthenticatedOrReadOnly,)
	def get_queryset(self):
		return self.queryset.filter(course_id = self.kwargs.get('course_id'))
	
	def perform_create(self, serializer):
		course = get_object_or_404(
			Courses, pk = self.kwargs.get('course_id')
			)
		serializer.save(course = course)

class RetrieveUpdateDestoryReview(generics.RetrieveUpdateDestroyAPIView):
	queryset = Review.objects.all()
	serializer_class = serializers.ReviewSerializer
	permission_classes = (IsAuthenticatedOrReadOnly,)




class CourseViewset(viewsets.ModelViewSet):
	queryset = Courses.objects.all()
	serializer_class = serializers.CoursesSerializer
	permissions_class = (IsAuthenticatedOrReadOnly,)
	search_fields = ('title',)

	@action(detail=True, methods=['get'])
	def reviews(self, request, pk =None):
		self.pagination_class = ReviewCustomPagination
		self.pagination_class.page_size = 1
		reviews = Review.objects.filter(course_id = pk)
		
		page = self.paginate_queryset(reviews)

		if page is not None:
			serializer = serializers.ReviewSerializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = serializers.ReviewSerializer(
			reviews, many=True )
		return Response(serializer.data)

class ReviewViewset(viewsets.ModelViewSet):
	queryset = Review.objects.all()
	serializer_class = serializers.ReviewSerializer
	permissions_class = (IsAuthenticatedOrReadOnly,)















# class ListCourseView(APIView):
# 	serializer_class = serializers.CoursesSerializer
# 	def get(self, request, format = None):
# 		courses = Courses.objects.all()
# 		serializer = self.serializer_class(courses, many=True)
# 		return Response(serializer.data)

# 	def post(self, request, format = None):
# 		serializer = self.serializer_class(data=request.data)
# 		serializer.is_valid(raise_exception=True)
# 		serializer.save()
# 		return Response(serializer.data, status=status.HTTP_201_CREATED)