from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon, Refund
from django.views.generic import (ListView,DetailView, CreateView, UpdateView,
        DeleteView,View )
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm, CouponForm, RefundForm
from django.conf import settings
from django.core.paginator import Paginator
import stripe
import random
sr = random.SystemRandom()
import string

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc" #for testing 




def home(request):
    obj = Item.objects.all()
    paginator = Paginator(obj,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list':obj,
        'page_obj': page_obj,
    }
        
    return render(request, 'home.html', context)


def Product(request,slug):
    
    context = {
        'object':Item.objects.get(slug=slug),
        'path':str(request.path).replace('/','9699699'),
    }
    return render(request,'product.html',context)


def categoryView(request,category):
    
    if 'shirt' in category.lower():
        search="S"
    elif 'sports-wear' in category.lower():
        search="SW"
    elif 'out-wear' in category.lower():
        search="OW"
    elif 'all' in category.lower():
        search="ALL"
    try:
        if search == "ALL":
            object = Item.objects.all()
            category = "all"
        else:
            object = Item.objects.filter(category=search)
        context = {
            'object_list':object,
            'category':category,
        }
    except:
        messages.error(request,"Invalid Category")
        return redirect('core:home')
    
    return render(request,'product-categorywise.html',context)

@login_required(login_url="account_login")
def add_to_cart(request,slug,redslug=None):
    #redirect slug setion 
    
    if redslug != None:
        if 'cart-summary' in redslug:
            final_red_slug = '/cart-summary/'
        elif 'product' in redslug:
            final_red_slug = f'/product/{slug}/'
        else:
            final_red_slug = '/'
    
    #add to cart 
    if request.user.is_authenticated:
        item = get_object_or_404(Item, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered = False,
        )
        order = get_user_order(request)
    
        if order:
            if order.items.filter(item__slug=item.slug).exists():
            
                order_item.quantity+=1
                order_item.save()
            else:
                order.items.add(order_item)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user = request.user,
                ordered_date=ordered_date,
            )
            order.items.add(order_item)
        messages.info(request,"Added To Cart")
    else:
        messages.info(request,"You Need to be logged In")
    return HttpResponseRedirect(final_red_slug)




@login_required
def remove_from_cart(request,slug,redslug=None):
    if redslug != None:
        if 'cart-summary' in redslug:
            final_red_slug = '/cart-summary/'
        elif 'product' in redslug:
            final_red_slug = f'/product/{slug}/'
        else:
            final_red_slug = '/'
            
    if request.user.is_authenticated:
        item = get_object_or_404(Item, slug=slug)
        order = get_user_order(request)
    
        if order:
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered = False,
                )[0]
                
                if order_item.quantity>0:
                    if order_item.quantity==1:
                        order.items.remove(order_item)
                        order_item.delete()
                    else:
                        order_item.quantity-=1
                        order_item.save()
                        
                count = order.items.count()
                if count==0:
                    order.delete()
                    
                messages.info(request,"Item removed from your cart")
            else:
                messages.info(request,"You don't have this item on your cart")
        else:
            messages.info(request,"You don't have active cart")
    else:
        messages.info(request,"You Need to be logged In")
        
    return HttpResponseRedirect(final_red_slug)


@login_required
def delete_from_cart(request,slug,redslug=None):
    if redslug != None:
        if 'cart-summary' in redslug:
            final_red_slug = '/cart-summary/'
        elif 'product' in redslug:
            final_red_slug = f'/product/{slug}/'
        else:
            final_red_slug = '/'
            
    if request.user.is_authenticated:
        item = get_object_or_404(Item, slug=slug)
        order = get_user_order(request)
    
        if order:
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered = False,
                )[0]
                
                order.items.remove(order_item)
                order_item.delete()
                        
                count = order.items.count()
                if count==0:
                    order.delete()
                    
                messages.info(request,"Product Deleted from your cart")
            else:
                messages.info(request,"You don't have this item on your cart")
        else:
            messages.info(request,"You don't have active cart")
    else:
        messages.info(request,"You Need to be logged In")
        
    return HttpResponseRedirect(final_red_slug)


class Checkout(LoginRequiredMixin,View):
    def get(self,request, *agrs, **kwargs):
        form = CheckoutForm(instance=get_initial_billing_data(request))
        #coupon
        couponform=CouponForm
        
        try:
            qs = get_user_order(request)
            context = {
                'form': form,
                'couponform':couponform,
                'object':qs
            }
        except:
            context = {
                'form': form,
                'couponform':couponform,
                'object':None,
            }
        return render(self.request,'checkout.html',context)

    def post(self,request, *agrs, **kwargs):
        try:
            qs = get_user_order(request)
        except:
            messages.warning(self.request,"Your Cart Is empty, Please add product to checkout")
            return redirect("/")
        else:
            
            form = CheckoutForm(self.request.POST or None, instance=get_initial_billing_data(request))
            form.instance.user = request.user
            if form.is_valid():
                form.save()
                payment_choice = form.cleaned_data.get('payment_method')
                if payment_choice == 'C':
                    return redirect('core:payment',method='card')
                if payment_choice == 'P':
                    return redirect('core:payment',method='Paypal')
                else:
                    return redirect('core:payment',method='Payoneer')
                
            messages.warning(self.request,"Wrong Input") 
            return redirect("core:checkout")
   
class CartSummary(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            qs = get_user_order(request)
            context = {
                'object':qs,
                'time':timezone.now(),
                'path':str(self.request.path).replace('/','9699699'),
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            context = {
                'object':None,
                'time':timezone.now(),
                'path':str(self.request.path).replace('/','9699699'),
            }
            return render(self.request,'order_summary.html',context)
            return redirect("/")
        
class PaymentView(LoginRequiredMixin,View):
    def get(self,request, *args, **kwargs):

        #checking if user added billing address
        if get_initial_billing_data(request) !=None:
            return render(request,'payment.html')
        else:
            return redirect('core:checkout')
        
    def post(self,request, *args, **kwargs):
        
        #checking if user added billing address
        if get_initial_billing_data(request) == None:
            return redirect('core:checkout')
        
        order = get_user_order(request)
        token = request.POST.get('tok_mastercard')
        amount= int(order.get_total_bill())
        charging = True
        # stripe charging 
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
            )
            charging = True
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            messages.error(request,f"{e.error.message}")
            pass
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request,f"{e.error.message}")
            pass
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request,f"{e.error.message}")
            pass
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request,f"{e.error.message}")
            pass
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request,f"{e.error.message}")
            pass
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(request,f"{e.error.message}")
            pass
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(request,f"{e.error.message}")
            pass
        

        
        if charging:

            payment = Payment()
            payment.amount = amount
            payment.status = True
            payment.user = request.user
            payment.save()

            #update the order_item ordered
            order_item = order.items.all()
            for item in order_item:
                item.ordered=True
                item.save()
                
            #order completing
            order.ordered = True
            order.payment = payment
            order.refrence_code = get_ref_code(request)
            order.save()
            
            
            messages.info(request,f"Your Have Ordered Successfully: order code: \"{order.refrence_code}\" <save it>")
            return redirect('/')
        else:
            return redirect('/')

def get_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except:
        return None
    
class CouponView(LoginRequiredMixin,View):
    
    def post(self, request, *args, **kwargs):
        form = CouponForm(request.POST or None)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            order = get_user_order(request)
            if order:
                temp = get_coupon(request,code)
                if temp != None:
                    order.coupon = temp
                    order.save()
                else:
                    messages.error(request,'Coupon Code invalid')
                    return redirect('core:checkout')
                
                messages.info(request,'Successfully coupon added')
                return redirect('core:checkout')
            else:
                messages.error(request,'You need to have order to appply coupon')
                return redirect('core:checkout')
        
def get_initial_billing_data(request):
    
    billing = BillingAddress.objects.filter(user=request.user).last()
    if billing:
        return billing
    else:
        return None
    
    
def get_user_order(request, status=None):
    
    if status:
        try:
            order = Order.objects.filter(user=request.user, ordered=True).last()
        except:
            return None
        
        if order:
            return order
        else:
            return None
    else:    
        try:
            order = Order.objects.filter(user=request.user, ordered=False).last()
        except:
            return None
        
        if order:
            return order
        else:
            return None
    
    
    
    
def get_ref_code(request):
    
    return f'{request.user}'+'-'+''.join(sr.choices(string.ascii_lowercase + string.digits, k=15))

def search(request):
    context={}
    if request.GET:
        query=request.GET['q']
        queries = query.split(' ')
    queryset = []
    try:
        for q in queries:
            product = Item.objects.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(additional_info__icontains=q) |
                Q(category__icontains=q)
            )
        for pro in list(set(product)):
            queryset.append(pro)
        
        #if query exist
        if list(set(queryset)):
            context = {
            'query': list(set(queryset)),
            'query_str':str(query),
            'num':len(list(set(queryset)))
        }
        #if query don't exist
        else:
            context = {
            'notfound':True,
            'query_str':str(query),
        }
            
    except:
        #any exception during search
        context = {
         'notfound':True,
        'query_str':str(query),
        }
        
    return render(request, 'home.html', context)



class RefundCreate(LoginRequiredMixin,CreateView):
    model = Refund
    form_class = RefundForm
    template_name = 'refund.html'
    success_url = '/'
    
    def form_valid(self, form):
        order = get_user_order(self.request,status=True)
        
        if form.cleaned_data.get('code') == order.refrence_code:
            form.instance.order=order
            order.refund_request=True
            order.save()
            return super().form_valid(form)
        
@login_required(login_url="account_login")
def completedOrders(request):
    ordered = Order.objects.filter(user=request.user,ordered=True)
    
    context = {
        "objects":ordered,
    }
    return render(request,'ordered.html',context)

@login_required(login_url="account_login")
def seeCompletedOrder(request,ref):
    ordered = Order.objects.get(user=request.user,ordered=True,refrence_code=ref)
    print(ordered)
    context = {
        "object":ordered,
    }
    return render(request,'see-order.html',context)
    