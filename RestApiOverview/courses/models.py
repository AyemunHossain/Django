from django.db import models

class  Courses(models.Model):
	title = models.CharField(max_length=255)
	url = models.SlugField(unique=True)

	def __str__(self):
		return self.title

class Review(models.Model):
	course = models.ForeignKey(Courses, on_delete=models.CASCADE,
								 related_name="reviews",related_query_name="reivew")
	name = models.CharField(max_length=50)
	email = models.EmailField()
	comment = models.TextField()
	rating = models.IntegerField()

	class Meta:
		unique_together = ['email','course']

	def __str__(self):
		return f"{self.rating} by {self.email} for {self.course}"