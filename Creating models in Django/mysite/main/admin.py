from django.contrib import admin
from .models import News
# Register your models here.

class NewsAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Tittle', {'fields': ['news_title']}),
        ('Author/Date', {'fields': ['news_author', 'news_published']}),
        ('News Content', {'fields': ['news_content']}),
    ]


admin.site.register(News,NewsAdmin)
