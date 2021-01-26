from rest_framework.views import APIView
from rest_framework.response import Response

class HelloApiView(APIView):
	
	def get(self, request, format = None):

		an_apiview = [
		"This is a simple api view",
		"Here i am just trying to demonstrate how api call works",
		"So you can add here any functionality as you want",
		":) Peace"
		]

		return Response({"message":"Hey there","an_apiview":an_apiview})