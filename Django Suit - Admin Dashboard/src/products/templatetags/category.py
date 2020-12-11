from django import template
from products.models import Category

register = template.Library()


@register.simple_tag
def get_category_to_product(pid):
	path_list=[]
	try:
		_category = Category.objects.get(product__id = pid)
		path_list+= _category.get_ancestors(ascending=False, include_self=True)
		
		return path_list
	except:
		return 

@register.simple_tag
def all_category():
	return Category.objects.all()