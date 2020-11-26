from django.db import models

# Create your models here.

class Products(models.Model):
	title = models.TextField(null=True)
	img =   models.ImageField(null=True, blank=True)
	class Meta:
		verbose_name_plural = "Products"
	def __str__(self):
		return self.title
