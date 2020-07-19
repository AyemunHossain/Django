from django import template 
from core.models import Order
from django.contrib.auth.decorators import login_required

register = template.Library()

@login_required
@register.simple_tag
def product_cart_item_count(user,slug):
    obj = Order.objects.filter(user__username=user,ordered=False)
    if obj.exists():
        obj2 = obj[0].items.filter(item__slug=slug)
        if obj2.exists():
            return obj2[0].quantity
    return 0