from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	image = models.ImageField(default='demo_profile.jpeg',upload_to=f'profile_picture/%Y/%m/%d/')

	class Meta:
	    verbose_name_plural = "User Profiles"

	def __str__(self):
		return f"{self.user.username} profile"

	def save(self,*args,**kwargs):

		super(Profile,self).save(*args,**kwargs)

		if self.pk != None and self.image:
			img = Image.open(self.image.path)
			if img.height > 300 or img.width >300:
				output_size = (300,300)
				img.thumbnail(output_size)
				img.save(self.image.path)