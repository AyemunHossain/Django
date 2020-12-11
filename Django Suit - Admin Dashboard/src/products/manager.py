from django.db import models


class ProductsQuery(models.QuerySet):
    # def get_merchant_product(): for this you need merchant app   #hashtag advance stuff
    
    def lower_than(self,price:int):
        return self.filter(price__lte=price)
    def grater_than(self,price:int):
        return self.filter(price__gte=price)
    
    def in_between(self, lPrice:int, uPrice:int):
        return self.filter(models.Q(price__gte=lPrice) & models.Q(price__lte=uPrice))
    
    def featured(self):
        return self.filter(featured=True)
    
class ProductsManager(models.Manager):
    def get(self):
        return ProductsQuery(self.model, using=self._db)
    
    def lower_than(self,price:int):
        return self.get().lower_than(price)
    
    def in_between(self, lPrice:int, uPrice:int):
        return self.get().in_between(lPrice, uPrice)
    
    def grater_than(self,price:int):
        return self.get().grater_than(price)
    
    def featured(self):
        return self.get().featured()