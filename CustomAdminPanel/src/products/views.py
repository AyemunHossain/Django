from django.shortcuts import render, redirect, HttpResponseRedirect
from .customForms import ProductCreationForm, ReviewForm, ExtraImage
from .models import Products, Image, Category, Review
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (DetailView, CreateView, UpdateView,
                                  DeleteView, View)
from django.conf import settings
from django.forms import modelformset_factory
from django.db.models import Q
from django.http import JsonResponse
from Merchant.models import Merchant
# Create your views here.


def homeView(request):
    products = None
    try:
        products = Products.objects.all()
    except:
        products = None
    return render(request, 'home.html', {'products': products, 'MEDIA_URL': settings.MEDIA_URL})


class productDetail(DetailView):
    model = Products
    template_name = 'products/product-page.html'

    def get_context_data(self, **kwargs):
        context = super(productDetail, self).get_context_data(**kwargs)

        try:
            product = Products.objects.filter(id=self.object.id)[0]
            comments = product.reviews.all()
            count = comments.count()
            context['comments'] = comments
            context['count'] = count
        except:
            context['comments'] = None
            context['count'] = None

        return context

class ProductCreation(LoginRequiredMixin, CreateView):
    model = Products
    fields = ['title', 'category', 'image', 'price',
              'description', 'additional_info', 'featured']
    template_name = 'Products/product-create.html'
    success_message = 'Product Added Successfully'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ProductCreation, self).get_context_data(**kwargs)

        context['form2'] = ExtraImage(
                            queryset=Image.objects.none())
        return context

    def form_valid(self, form,):
        
        
        form.instance.merchant = Merchant.objects.get(user=self.request.user)
        
        form_set = ExtraImage(self.request.POST or None,
                              self.request.FILES or None)
        if self.request.POST:
            if form.is_valid() and form_set.is_valid():
                product = form.save()
                for form in form_set:
                    temp = form.cleaned_data.get("images")
                    if temp != None:
                        image = Image(product=product, images=temp)
                        image.save()

                return super().form_valid(form)
            return super().form_invalid(form)


class ProductUpdate(View):
    
    def post(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        form = ProductCreationForm(self.request.POST, self.request.FILES, instance=Products.objects.filter(slug=slug).first())
        form_set = ExtraImage(self.request.POST or None, self.request.FILES or None)
        
        product = Products.objects.filter(slug=slug).first()
        
        if form.is_valid() and form_set.is_valid():
            form.save()
            obj = Image.objects.filter(product=product)

            for index, form in enumerate(form_set):
                temp = form.cleaned_data.get("images")
                id = self.request.POST.get(f'form-{index}-id')

                if temp !=None and temp != False:
                    temp_obj = None
                    try:
                        temp_obj = Image.objects.get(product_id=product.id,id=id)
                    except:
                        pass
                    if temp_obj != None:
                        #updating pic
                        image = Image(product_id=product.id, images=temp)
                        temp_obj.images = image.images
                        temp_obj.save()
                    else:
                        #new pic
                        image = Image(product_id=product.id, images=temp)
                        image.save()
                elif temp == False:
                    #delete pic
                    image = Image.objects.get(product_id=product.id, id=id)
                    image.delete()
                    
        return redirect('/')
    
    def get(self, * args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = Products.objects.filter(slug= slug).first()
        form = ProductCreationForm(instance=instance)
        context = {}
        context['form'] = form
        context['form2'] = ExtraImage(
            queryset=Image.objects.filter(product_id=instance.id))
        return render(self.request, 'Products/product-update.html', context)


class ProductDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Products
	context_object_name = "product"
	template_name = 'Products/productDelete.html'
	success_message = "Product Deleted"
	success_url = '/'


def search(request):
    context = {}
    query_set = set()

    try:
        qr = request.GET.get('query')
        _category = str(request.GET.get('category')).lower()
        
        if str(_category).lower() == 'all':

            if qr == None or qr == '':
                products = Products.objects.all()
                context['products'] = products
                return render(request, "search.html", context)

            else:
                qr = str(qr).split('+')
                for q in qr:
                    products = Products.objects.filter(
                        Q(title__icontains=q) |
                        Q(description__icontains=q) |
                        Q(additional_info__icontains=q) |
                        Q(category__title__icontains=q) |
                        Q(product_code__icontains=q)
                    )
                context['products'] = products
                return render(request, "search.html", context)

        else:

            if qr == None or qr == '':
                products = Products.objects.filter(
                category__title__icontains=_category)
                context['products'] = products
                return render(request, "search.html", context)

            products = Products.objects.filter(
                Q(category__title__icontains=_category) &
                (
                    Q(title__icontains=qr) |
                    Q(description__icontains=qr) |
                    Q(additional_info__icontains=qr) |
                    Q(label__icontains=qr) |
                    Q(product_code__icontains=qr)
                )
                
            )
            context['products'] = products
            return render(request, "search.html", context)

    except:
        pass

    return render(request, "search.html")


class CreateReview(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        temp = Review.objects.filter(
            Q(product__slug=slug) &
            Q(user=self.request.user)
        )
        if temp.exists():
            messages.warning(request, "You Have Already Reviewed this product")
            url = self.request.META.get("HTTP_REFERER")
            return HttpResponseRedirect(url)

        else:
            form = ReviewForm(request.POST)
            form.instance.user = request.user
            product = Products.objects.filter(slug=slug)[0]
            form.instance.product = product
            if form.is_valid():
                form.save()

            messages.info(request, "Your Review is added")

            url = self.request.META.get("HTTP_REFERER")
            return HttpResponseRedirect(url)

#review update is remain for leter

def autoSearch(request):

    if 'term' in request.GET:
        q = request.GET.get('term')
        product = Products.objects.filter(title__icontains=q)
        results = []
        for pl in product:
         results.append(pl.title)

        return JsonResponse(results, safe=False)