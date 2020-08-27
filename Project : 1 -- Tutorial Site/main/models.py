from django.db import models


class TutorialCategory(models.Model):
	tutorial_category = models.CharField(max_length=200)
	category_summary = models.CharField(max_length=200)
	category_slug = models.CharField(max_length=200,default=1)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.tutorial_category
		
class TutorialSeries(models.Model):
	tutorial_series = models.CharField(max_length=200)
	series_summary = models.CharField(max_length=200)
	tutorial_category = models.ForeignKey(TutorialCategory, default=1, verbose_name="Category",on_delete = models.SET_DEFAULT)

	class Meta:
		verbose_name_plural = "Series"

	def __str__(self):
		return self.tutorial_series


# Create your models here.
class Tutorials(models.Model):
	tutorial_title = models.CharField(max_length=200)
	tutorial_content = models.TextField()
	tutorial_date = models.DateTimeField("Published Date")
	tutorial_series = models.ForeignKey(TutorialSeries,default=1, verbose_name="Series", on_delete = models.SET_DEFAULT)
	tutorial_slug = models.CharField(max_length=200,default=1)

def __str__(self):
	return self.tutorial_title