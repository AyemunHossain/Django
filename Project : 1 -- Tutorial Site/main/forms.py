from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UC_form(UserCreationForm):
	first_name = forms.CharField(required=True,max_length=50,help_text="First Name")
	last_name = forms.CharField(required=True,max_length=50,help_text="Last Name")
	email = forms.EmailField(required=True,max_length=50,help_text="Required a valid Email Address")

	class Meta:
		model = User
		fields = ('first_name','last_name','email','username','password1','password2')

	def save(self,commit=True):
		user = super(UC_form,self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user
		



