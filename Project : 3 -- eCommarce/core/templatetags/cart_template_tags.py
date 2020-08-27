from django import template 
from core.models import Order 

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        count = Order.objects.filter(user=user,ordered=False)
        if count.exists():
            return count[0].items.count()
        return 0