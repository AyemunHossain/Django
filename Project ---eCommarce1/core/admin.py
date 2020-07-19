from django.contrib import admin
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon, Refund



def make_refund(modeladmin, request, queryset):
    queryset.update(refund_request=False, refund_granted=True)
make_refund.short_description="Apporve refund"

class ItemAdmin(admin.ModelAdmin):
    
    
    list_display = ('title','price','discount_price', 'category','featured','created','modified')
    list_display_links = ('title','price','created',)
    search_fields = ('title','price','description')
    readonly_fields = ('slug','created','modified')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
            ("Product Details",{'fields':('title','image','image1','image2','image3','price','discount_price','description','additional_info')}),
            
            ("Product Permission/Others",{'fields':('category','label','featured','slug','created','modified')}),
        )
    

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('user','item','ordered','quantity')
    list_display_links = ('user','item',)
    search_fields = ('user__username','item__title',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
            ("Order Status/Others",{'fields':('user','item','ordered','quantity')}),
        )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','refrence_code','ordered_date','get_total_bill','get_total_saving','coupon',
                    'ordered','delivering','recieved','refund_request','refund_granted',)
    
    list_display_links = ('user','refrence_code','ordered_date','get_total_bill','get_total_saving',)
    search_fields = ('user__username','items__item__title','ordered_date')
    readonly_fields = ('start_date','get_total_bill','get_total_saving',)
    filter_horizontal = ()
    list_filter = ('coupon','delivering','recieved','refund_request','refund_granted')
    fieldsets = (
            ("Order Info",{'fields':('user','items','payment','coupon','get_total_bill','get_total_saving',)}),
            ("Order Details",{'fields':('start_date','ordered_date','ordered','billing_address')}),
            ("Order Status",{'fields':('delivering','recieved','refund_request','refund_granted')})
        )
    actions=[make_refund]
   
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)