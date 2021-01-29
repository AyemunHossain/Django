from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Firstapi import serializers
from rest_framework import viewsets


class HelloApiView(APIView):
	serializer_class = serializers.HelloSerializer
	def get(self, request, format = None):

		an_apiview = [
		"This is a simple api view",
		"Here i am just trying to demonstrate how api call works",
		"So you can add here any functionality as you want",
		":) Peace"
		]
		return Response({"message":"Hey there","an_apiview":an_apiview})

	def post(self, request):
		serializer = self.serializer_class(data = request.data)
		if serializer.is_valid():
			name = serializer.validated_data.get("name")
			message = f"Hello {name}"
			return Response({"message":message})
		else:
			return Response(
				serializer.errors,
				status = status.HTTP_400_BAD_REQUEST
				)

	def put(self, request, pk = None):
		return Response({"message":"This is put request"})

	def patch(self, request, pk = None):
		return Response({"message":"This is patch request"})

	def delete(self, request, pk = None):
		return Response({"message":"This is delete request"})


class HelloViewSet(viewsets.ViewSet):

	serializer_class = serializers.HelloSerializer
	
	def list(self, request):
		a_viewset = [
			"Uses actions (list,create, retrive,update, partial_update)",
		]

		return Response({"message": "Hello","a_viewset": a_viewset})

	def create(self, request):

		serializer = self.serializer_class(data = request.data)
		if serializer.is_valid():
			name = serializer.validated_data.get("name")
			message = f"Hello {name}"
			return Response({"message":message})
		else:
			return Response(
				serializer.errors,
				status = status.HTTP_400_BAD_REQUEST
				)

	def retrieve(self, request, pk=None):

		return Response({"http-method":"GET"})

	def update(self, request, pk=None):

		return Response({"http-method":"PUT"})

	def partial_update(self, request, pk=None):

		return Response({"http-method":"PATCH"})

	def destroy(self, request, pk=None):

		return Response({"http-method":"DELETE"})