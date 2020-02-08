from django.contrib import admin
from .models import News
from tinymce import TinyMCE
from django.db import models
# Register your models here.

class NewsAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Tittle',{'fields':['news_title']}),
        ('Author/Date',{'fields':['news_author','news_published']}),
        ('News Content',{'fields':['news_content']}),
    ]
    formfield_overrides = {
        models.TextField:{'widget':TinyMCE}

    }

admin.site.register(News,NewsAdmin)