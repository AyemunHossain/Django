from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from .models import Profile 


class customUserCreationForm(UserCreationForm):
	first_name = forms.CharField(required=True, max_length=50)
	last_name = forms.CharField(required=True, max_length=50)
	email = forms.EmailField(required=True, max_length=50,help_text="Required a valid Email Address")
	
	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password1','password2']


	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
		    raise forms.ValidationError("Email exists")
		return email


	def save(self,commit=True):
		user = super(customUserCreationForm,self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user



class UpdateProfileInfo(forms.ModelForm):

	first_name = forms.CharField(required=True, max_length=50)
	last_name = forms.CharField(required=True, max_length=50)
	email = forms.EmailField(required=True, max_length=50,help_text="Required a valid Email Address")
	
	class Meta:
		model = User
		fields = ['username','first_name','last_name','email']


	def clean_email(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		
		try:
			user = User.objects.filter(username=username).first()
			if User.objects.filter(email=email).exists():
				if user.email != email:
					raise forms.ValidationError("Email exists")
		except:
			if User.objects.filter(email=email).exists():
				raise forms.ValidationError("Email exists")
		
		return email
		
	
	def save(self,commit=True):
		user = super(UpdateProfileInfo,self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

		return user

class UpdateProfilePicture(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['image']