from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

PAYMENT_CHOICES = (
    ('C',"Credit Card/Master Card"),
    ('P','Paypal'),
    ('Py','Payoneer'),
    
)
CATEGORY_CHOICES =(
	('S', 'Shirt'),
	('SW','Sports Wear'),
	('OW','Out Wear'),
)

LABEL_CHOICES =(
	('P', 'primary'),
	('S','secondary'),
	('D','danger'),
)

class Item(models.Model):
	title 			= models.CharField(max_length = 450, default='Default title !!!')
	image 			= models.ImageField(blank=True, null=True, default = 'ProductsDefault.jpg',upload_to = 'Products/%Y/%m/%d/',verbose_name="Main Image")
	image1 			= models.ImageField(blank=True, null=True, upload_to = 'Products/%Y/%m/%d/',verbose_name="2nd Image")
	image2 			= models.ImageField(blank=True, null=True, upload_to = 'Products/%Y/%m/%d/',verbose_name="3rd Image")
	image3 			= models.ImageField(blank=True, null=True, upload_to = 'Products/%Y/%m/%d/',verbose_name="4th Image")
 
	price 			= models.DecimalField(decimal_places=2, max_digits=20, default=0,verbose_name="Product Price",validators=[MinValueValidator(0.0)])
	discount_price  = models.DecimalField(blank=True,null=True,decimal_places=2, max_digits=20, verbose_name="Discount Price",validators=[MinValueValidator(0.0)]) 
	slug 			= models.SlugField(blank=True,unique=True)
	description 	= RichTextField()
	additional_info = RichTextField(blank=True,null=True)
	category		= models.CharField(choices=CATEGORY_CHOICES, max_length=2)
	label			= models.CharField(choices=LABEL_CHOICES, max_length=1)
		
 
	featured		= models.BooleanField(default=False, verbose_name="Featured Product")
	created			= models.DateTimeField(auto_now_add=True)
	modified 		= models.DateTimeField(auto_now=True)
	history			= HistoricalRecords()
	
	class Meta:
		ordering = ['-created']
		verbose_name_plural = 'Item'
	
	def __str__(self):
		return self.title

	def __unicode__(self):
	    return self.title
	def get_absolute_url(self):
		return reverse("core:product",kwargs={'slug':self.slug})

	def add_to_cart_url(self, path):
		return reverse("core:add_to_cart",kwargs={'slug':self.slug,'redslug':path},)
    
	def remove_from_cart_url(self,):
    		return reverse("core:remove_from_cart",kwargs={'slug':self.slug})

	def cart_delete_url(self):
		return reverse("core:delete_from_cart",kwargs={'slug':self.slug})
     

class OrderItem(models.Model):
    user		= models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    item 		= models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered     = models.BooleanField(default = False)
    quantity 	= models.IntegerField(default=1,validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def get_total_item_price(self):
        if (self.item.discount_price != None) and (self.item.discount_price > 0):
            return (self.quantity*self.item.discount_price)
        else:
            return (self.quantity*self.item.price)
	
    def get_saved_amount(self):
         if (self.item.discount_price != None) and (self.item.discount_price > 0):
            return (self.quantity*self.item.price)-self.get_total_item_price()
         else:
             return None
			 
             
             
class Order(models.Model):
    user 			= models.ForeignKey(User,on_delete=models.CASCADE)
    items 			= models.ManyToManyField(OrderItem)
    refrence_code   = models.CharField(max_length=50, unique=True)
    start_date  	= models.DateTimeField(auto_now_add = True)
    ordered_date	= models.DateTimeField()
    ordered 		= models.BooleanField(default = False)
    billing_address = models.ForeignKey('BillingAddress', null=True, blank=True,
                                on_delete=models.SET_NULL)
    payment         = models.ForeignKey('Payment', null=True, blank=True,
                                on_delete=models.SET_NULL)
    coupon          = models.ForeignKey('Coupon', null=True, blank=True,
                                on_delete=models.SET_NULL)
    
    delivering      = models.BooleanField(default = False)
    recieved        = models.BooleanField(default = False)
    refund_request  = models.BooleanField(default = False)
    refund_granted  = models.BooleanField(default = False)
    
    def __str__(self):
        return f"{self.refrence_code}"

    def get_total_bill(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        if self.coupon:
            total -=int(self.coupon.amount)
        return total
    
    def get_total_saving(self):
        total = 0
        for order_item in self.items.all():
            if order_item.get_saved_amount():
            	total += order_item.get_saved_amount()
        if total ==0:
            return None
        return total

class BillingAddress(models.Model):
    user 					= models.ForeignKey(User,on_delete=models.CASCADE)
    address 				= models.CharField(max_length=300)
    apartment_address 		= models.CharField(max_length = 200)
    country 				= CountryField(multiple=False)
    zipcode 				= models.CharField(max_length=5)
    same_billing_address 	= models.BooleanField(default=False)
    save_info 				= models.BooleanField(default=False)
    payment_method 			= models.CharField(choices=PAYMENT_CHOICES, max_length=2)
    
    
    def __str__(self):
        return f"{self.user.username}'s Billing Address"

class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.FloatField()
    class Meta:
        ordering = ['amount']
    
    def __str__(self):
        return self.code 
    
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True )
    stripe_charge_id = models.CharField(max_length=50,null=True, blank=True )
    amount = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
class Refund(models.Model):
    order       = models.ForeignKey('Order', on_delete=models.CASCADE)
    reason      = models.TextField()
    review      = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.order.refrence_code
    