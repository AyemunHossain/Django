from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .customForms import (customUserCreationForm, UpdateProfileInfo, 
	  UpdateProfilePicture
	)
from django.contrib.auth import views as auth_views
from django.views.generic import ListView
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.auth.forms import AuthenticationForm

def login_page(request):
	if request.method == "POST":
		form = AuthenticationForm(request,request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")


			user = authenticate(username=username,password=password)

			if user is not None:
				login(request,user)
				request.session['last_hit'] = json.dumps(datetime.strftime(
                                        datetime.now(), '%Y-%m-%d %H:%M:%S.%f'))

				messages.success(request,f"{username} logged in Successfully")
				return redirect("users:userProfile")
			else:	
				messages.error(request,"Invalid UserName or Password")

		else:
			messages.error(request,"Invalid UserName or Password")

	form = AuthenticationForm
	return render(request=request,
					template_name='users/login.html',
					context={'form':form})


def userLogout(request):
	if request.user.is_authenticated:
		logout(request)
		messages.info(request,"Logout Successfully")
		return render(request,'users/logout.html')

	else:
		messages.info(request,'Please Login First')
		return redirect('blogPosts:homePage')

def userSignup(request):
	if request.user.is_authenticated:
		messages.info(request,"Already Registred")
		return redirect('blogPosts:homePage')
	else:
		if request.method =="POST":
			form = customUserCreationForm(request.POST)
			if form.is_valid():
				user = form.save()
				messages.info(request,"Account Created")
				login(request,user)
				messages.info(request,"Successfully Logged in")
				return redirect("blogPosts:homePage")
		else:
			form = customUserCreationForm
		
		return render(request,'users/signup.html',{'form':form})

@login_required
def userProfile(request):
	if request.user.is_authenticated:
		return render(request,'users/profile.html',{'user':request.user})
	return render(request,'blogPosts/home.html')

@login_required
def userProfileUpdate(request):
	if request.method == "POST":
		p_form = UpdateProfilePicture(request.POST,request.FILES, instance = request.user.profile)
		u_form = UpdateProfileInfo(request.POST, instance = request.user)

		if p_form.is_valid() and u_form.is_valid():
			p_form.save()
			u_form.save()
			messages.info(request,"Successfully profile updated")
			return redirect("users:userProfile")
	else:
		p_form = UpdateProfilePicture(instance = request.user)
		u_form = UpdateProfileInfo(instance = request.user)

	return render(request,"users/profileUpdate.html",{"p_form":p_form,"u_form":u_form})


class UserPublicProfile(ListView):
	model = User
	template_name = 'users/user_public_profile.html'
	context_object_name = 'user'

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return User.objects.filter(username=user).first()
