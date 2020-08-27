from django.db.models.signals import pre_save 
from .models import Item
from django.dispatch import receiver 
from django.utils.text import slugify
import random, string

sr = random.SystemRandom()

@receiver(pre_save ,sender=Item)
def slug_creator(sender, instance, *agrs, **kwargs):
	if instance.history.last() is None:
		ch = sr.choices(string.digits,k=3)
		ch += sr.choices(string.ascii_letters,k=5)
		sr.shuffle(ch)
		ch = ''.join(ch)
		instance.slug = slugify(f"{instance.title}{ch}")
	