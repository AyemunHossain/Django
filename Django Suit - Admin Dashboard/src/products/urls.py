from django.urls import path 
from .import views
from django.contrib.auth.decorators import login_required

app_name = "Products"


urlpatterns = [
    
	path('',views.homeView,name='homeView'),
	path('product/create/',views.ProductCreation.as_view() ,name='productCreation'),
	path('product/<slug:slug>/',views.productDetail.as_view() ,name='productDetail'),
 	path('product/<slug:slug>/update/',views.ProductUpdate.as_view(), name="productUpdate"),
	path('search/',views.search,name="search"),
	path('review/<slug:slug>/', views.CreateReview.as_view(), name='review'),
	path('auto-search/', views.autoSearch, name='autosearch'),
]
