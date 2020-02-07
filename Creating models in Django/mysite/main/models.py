from django.db import models

# Create your models here. we added Tutorial model here 
class Tutorial(models.Model):
    tutorial_tittle = models.CharField(max_length=200)
    tutorial_content = models.TextField()
    tutorial_published = models.DateTimeField("Date published")

    def __str__(self):
        return self.tutorial_tittle