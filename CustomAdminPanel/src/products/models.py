from django.db import models
from django.urls import reverse
from .manager import ProductsManager
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, 	TreeForeignKey
from django.utils.safestring import mark_safe
from os.path import basename, splitext
from django.utils import timezone

#task-1 product image upload path :<neede category,marchant and others :)
User = get_user_model()

def image_upload_path(instance, filename):
    base_name = basename(filename)
    name, extension = splitext(base_name)
    if len(name) > 20:
        name = name[:19]
    time = timezone.now().strftime("%Y/%m")

    return f"Products/{time}/{name}{extension}"


class ProductBaseClass(models.Model):
	title 					= models.CharField(max_length=450, default='Default title !!!')
	category 				= models.ForeignKey('Category', on_delete=models.SET_DEFAULT,
								default=None, related_name='cat_products', related_query_name='product')
	
	image 					= models.ImageField(blank=True, null=True,
	                          max_length=500, upload_to=image_upload_path)

	price 					= models.DecimalField(decimal_places=2, max_digits=20, default=0,
	                            verbose_name="Product Price", validators=[MinValueValidator(0.0)])
	discount_price 			= models.DecimalField(blank=True, null=True, decimal_places=2,
	                                     max_digits=20, verbose_name="Discount Price", validators=[MinValueValidator(0.0)])

	slug 					= models.SlugField(blank=True, unique=True)
	description 			= models.TextField(null=True,)
	additional_info 		= models.TextField(null=True,)
	

	#i need to work on product code deeply :)
	product_code 			= models.CharField(max_length=50, null=True, blank=True)
	created 				= models.DateTimeField(auto_now_add=True)
	modified 				= models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Products(ProductBaseClass):
    
	STATUS = (
		('In Stock', 'In Stock'),
		('StockOut', 'StockOut'),
		('Unknown', 'Unknown')
	)
	LABEL_CHOICES = (
            ('New', 'New'),
            ('Hot', 'Hot'),
            ('Bestselling', 'Bestselling'),

        )
 
	average_rate 			= models.FloatField(default=0, null=True, blank=True)
	status 					= models.CharField(max_length=30, choices=STATUS,
                                	null=True, default='In Stock')
	label 					= models.CharField(choices=LABEL_CHOICES, max_length=20)
	featured 				= models.BooleanField(default=False, verbose_name="Featured Product")

	history 				= HistoricalRecords()
	objects 				= ProductsManager()

	class Meta:
		ordering = ['-created']
		verbose_name_plural = 'Products'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("Products:productDetail", kwargs={"slug": self.slug})

	def add_to_cart_url(self, path):
		pass

	def image_tag(self):
		try:
			if self.image.url is not None:
				return mark_safe(f"<img src={self.image.url} height='50'/>")
			else:
				return None
		except:
			return  


class Category(MPTTModel):
	parent 				= TreeForeignKey('self', on_delete=models.CASCADE,
	                    	    null=True, blank=True, related_name='children')
	title 				= models.CharField(max_length=200)
	image 				= models.ImageField(blank=True, upload_to='category/image/')
	slug 				= models.SlugField(unique=True)
	created 			= models.DateTimeField(auto_now_add=True)
	updated 			= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	class MPTTMeta:
		order_insertion_by = ['title']
		level_attr = 'mptt_level'
		abstract = False

	class Meta:
		verbose_name_plural = 'Categories'
		abstract = False

	def __str__(self):
		path = [self.title]
		temp_parent = self.parent
		while temp_parent is not None:
			path.append(temp_parent.title)
			temp_parent = temp_parent.parent
		return ' / '.join(path[::-1])


class Image(models.Model):
	product = models.ForeignKey(Products, on_delete=models.CASCADE,
	                            related_name="ProductsExtraImages", related_query_name="extraimages")
	images = models.ImageField(blank=True, null=True,
	                           max_length=500, upload_to=image_upload_path)
	short_description = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.product.title


class Review(models.Model):
	
	user = models.ForeignKey(User, on_delete=models.CASCADE,
	                         related_name="reviews", related_query_name="review")
	product = models.ForeignKey(Products, on_delete=models.CASCADE,
	                            related_name="reviews", related_query_name="review")
	comment = models.CharField(max_length=250, blank=True)
	
	rate = models.PositiveIntegerField(
	    default=0, validators=[MaxValueValidator(5)])
	
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.comment
