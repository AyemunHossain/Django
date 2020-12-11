from django import forms
from .models import Products, Review, Image


class ProductCreationForm(forms.ModelForm):

	class Meta:
		model = Products
		fields = [
			'title', 'image','price', 'description', 'additional_info', 'featured'
			]


class ImagesForm(forms.ModelForm):
    
	class Meta:
		model = Image
		fields = ['images']


ExtraImage = forms.modelformset_factory(Image, form=ImagesForm,
                    fields=('images',), extra=4, max_num=4)


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['comment','rate']
