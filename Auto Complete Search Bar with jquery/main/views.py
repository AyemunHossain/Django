from django.shortcuts import render, HttpResponse
from .models import Products
from django.http import JsonResponse



def home(request):

	if 'term' in request.GET:
		qr = Products.objects.filter(title__icontains = request.GET.get('term'))

		title = list()
		for products in qr:
			title.append(products.title)
		return JsonResponse(title, safe=False)

	return render(request,'main/home.html',{})