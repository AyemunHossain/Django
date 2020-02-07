from django.db import models

# Create your models here.

class News(models.Model):
    news_title = models.CharField(max_length=200)
    news_author = models.CharField(max_length=50)
    news_content = models.TextField()
    news_published = models.DateTimeField()

    def __str__(self):
        return self.news_title

