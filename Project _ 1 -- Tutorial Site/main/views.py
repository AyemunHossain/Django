from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tutorials, TutorialSeries, TutorialCategory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import UC_form

# Create your views here.
def single_slug_handler(request,single_slug):
	print(single_slug)
	all_category = [cat.category_slug for cat in TutorialCategory.objects.all()]
	if single_slug in all_category:
		all_series_on_category = TutorialSeries.objects.filter(tutorial_category__category_slug = single_slug)
		series_urls = {}
		for series in all_series_on_category.all():
			try:
				tut_part_one = Tutorials.objects.filter(tutorial_series__tutorial_series=series.tutorial_series).earliest("tutorial_date")
				series_urls[series] = tut_part_one.tutorial_slug	
			except:
				series_urls[series] =None

		return render(request,
					  'main/category_page.html',
					  context={'tut_part_one':series_urls}
					)
			

	all_tutorial = [tut.tutorial_slug for tut in Tutorials.objects.all()]
	
	if single_slug in all_tutorial:
		
		this_tutorial = Tutorials.objects.get(tutorial_slug=single_slug)
		series_all_tutorials = Tutorials.objects.filter(tutorial_series__tutorial_series = this_tutorial.tutorial_series).order_by("tutorial_date")
		
		current_tut_inx = list(series_all_tutorials).index(this_tutorial)

		return render(request,
					  'main/tutorial.html',
					  {'this_tutorial':this_tutorial,
					   'series_all_tutorials':series_all_tutorials,
					   'current_tut_inx':current_tut_inx,
					   })
	return HttpResponse("<p><font size='72'>404</font></p>")



def homepage(request):
	return render(request=request,
		template_name='main/home.html',
		context={"category": TutorialCategory.objects.all()})
    

def register(request):

	if request.method == "POST":
		form=UC_form(request.POST)
		if form.is_valid():
			user=form.save()
			username = form.cleaned_data.get('username')
			messages.info(request,f"{username} account created")
			login(request,user)
			messages.info(request,f"Successfully Logged in")
			return redirect('main:homepage')
		else:
			for msg in form.error_messages:
				messages.error(request,f"{form.error_messages[msg]}")

	form = UC_form
	return render(request=request,
				template_name='main/register.html',
				context={'form':form})


def logout_page(request):
	logout(request)
	messages.info(request,"Logged out successfully!")
	return redirect("main:homepage")



def login_page(request):
	if request.method == "POST":
		form = AuthenticationForm(request,request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")


			user = authenticate(username=username,password=password)

			if user is not None:
				login(request,user)
				messages.success(request,f"{username} logged in Successfully")
				return redirect("main:homepage")
			else:	
				messages.error(request,"Invalid UserName or Password")

		else:
			messages.error(request,"Invalid UserName or Password")

	form = AuthenticationForm
	return render(request=request,
					template_name='main/login.html',
					context={'form':form})

'''
def profile(request):
	if request.user.is_authenticated:
		#Working on it soon i will push it :)

'''	