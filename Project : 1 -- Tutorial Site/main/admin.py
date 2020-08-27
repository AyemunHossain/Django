from django.contrib import admin
from .models import Tutorials, TutorialSeries, TutorialCategory
from django.db import models
from tinymce import TinyMCE


# Register your models here.
class TutorialAdmin(admin.ModelAdmin):
			
	fieldsets = [
		("title_date",{"fields" : ["tutorial_title","tutorial_date"]}),
		("Urls",{"fields" : ["tutorial_slug"]}),
		("Tutorial Series",{"fields" : ["tutorial_series"]}),
		("Content",{"fields" : ["tutorial_content"]}),

	]

	formfield_overrides = {
		models.TextField : {'widget': TinyMCE() },
	}



admin.site.register(TutorialSeries)
admin.site.register(TutorialCategory)
admin.site.register(Tutorials, TutorialAdmin)