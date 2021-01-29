from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from userprofile import serializers
from userprofile import models 
from userprofile import permission

class UserProfileViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.ProfileSerializers
	queryset = models.Account.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permission.UpdateOwnProfile,)
	filter_backends = (filters.SearchFilter,)
	search_fields = ('username','email',)

class UserLoginApiView(ObtainAuthToken):
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedItemViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication, )
	serializer_class = serializers.ProfileFeedItemSerializer
	queryset = models.ProfileFeedItem.objects.all()
	permission_classes = (permission.UpdateProfileFeed, IsAuthenticated)

	def perform_create(self, serializers):
		serializers.save(user_profile = self.request.user)