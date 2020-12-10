from django.db.models.signals import pre_save, post_save
from django.db.models import Avg
from .models import Products, Category, Review
from django.dispatch import receiver 
from django.utils.text import slugify
import random, string

sr = random.SystemRandom()

@receiver(pre_save ,sender=Products)
def slug_creator(sender, instance, *agrs, **kwargs):
	if instance.history.last() is None:
		ch = sr.choices(string.digits,k=3)
		ch += sr.choices(string.ascii_letters,k=5)
		sr.shuffle(ch)
		ch = ''.join(ch)
		instance.slug = slugify(f"{instance.title}-{ch}")

@receiver(pre_save, sender=Category)
def category_slug(sender, instance, *args, **kwargs):

	try:
		parent_slug = instance.parent.slug
		if parent_slug:
			instance.slug = slugify(f"{parent_slug}-{instance.title}")
		else:
			instance.slug = slugify(instance.title)
	except:
		instance.slug = slugify(instance.title)
  
@receiver(post_save, sender=Review)
def average_review(sender, instance, *args, **kwargs):
	try:
		product 				= Products.objects.filter(id = instance.product_id )[0]
		review 					= product.reviews.all()
		avg 					= review.aggregate(avg=Avg("rate"))
		product.average_rate 	= round(avg['avg'],5)
		product.save()    
	except:
		pass

@receiver(pre_save, sender=Review)
def add_review(sender, instance, * args, **kwargs):
	_temp = Review.objects.filter(user=instance.user, product_id = instance.product_id)
	if _temp.exists():
		 raise Exception('User Already Reviewed')