from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class blogPost(models.Model):
	image = models.ImageField(blank=True, null=True,upload_to="post/%Y/%m/%d/")
	title = models.CharField(max_length=200)
	content = models.TextField()
	date = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blogPosts:postDetail', kwargs = {'pk':self.pk})

	def save(self,*args,**kwargs):

		if self.pk != None :
			super(blogPost,self).save(*args,**kwargs)
			
			if self.image:
				img = Image.open(self.image.path)
				if img.height > 200 or img.width >900:
					output_size = (200,900)
					img.thumbnail(output_size)
					img.save(self.image.path)

		if self.pk is None :
			super(blogPost,self).save(*args,**kwargs)

			if self.image != None:
				super(blogPost,self).save(*args,**kwargs)
				img = Image.open(self.image.path)
				if img.height > 200 or img.width >900:
					output_size = (200,900)
					img.thumbnail(output_size)
					img.save(self.image.path)
			

		
