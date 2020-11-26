from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.home,name='home'),
    path('product/<slug:slug>/',views.Product,name='product'),
    path('cart/<slug:slug>/',views.add_to_cart,name='add_to_cart'),
    path('cart-item-delete/<slug:slug>/',views.delete_from_cart,name='delete_from_cart'),
    path('cart-item-remove/<slug:slug>/',views.remove_from_cart, name ="remove_from_cart"),
    path('cart-summary/',views.CartSummary.as_view(),name='cart_summary'),
    path('checkout/',views.Checkout.as_view(), name='checkout'),
    path('payment/<str:method>/',views.PaymentView.as_view(), name='payment'),
    path('coupon/',views.CouponView.as_view(), name='coupon'),
    path('search/',views.search, name='search'),
    path('orders/',views.completedOrders, name='orders'),
    path('order/<str:ref>/',views.seeCompletedOrder, name='order'),
    path('refund/',views.RefundCreate.as_view(), name='refund'),
    path('category/<str:category>/',views.categoryView, name='category'),
    
    # path('label/<str:label>/',views.categoryView, name='category'),
    #With redirecting url
    path('cart/<slug:slug>/<str:redslug>/',views.add_to_cart,name='add_to_cart'), 
    path('cart-item-remove/<slug:slug>/<str:redslug>/',views.remove_from_cart, name ="remove_from_cart"),
    path('cart-item-delete/<slug:slug>/<str:redslug>/',views.delete_from_cart,name='delete_from_cart'),
] 