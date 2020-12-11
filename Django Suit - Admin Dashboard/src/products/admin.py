from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Products, Category, Image, Review
import admin_thumbnails
from fieldsets_with_inlines import FieldsetsInlineMixin

class ProductImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ('id',)
    extra = 3
    max_num = 10


class ProductsAdmin(FieldsetsInlineMixin, admin.ModelAdmin):
    model = Products
    list_display = ('title','category', 'price',
                    'discount_price', 'featured', 'created', 'status', 'image_tag')
    list_display_links = ('title', 'price', 'created',)
    list_editable = ('category', 'featured', 'status')
    list_per_page = 8
    search_fields = ('title', 'price', 'summary', 'description')
    readonly_fields = ('image_tag', 'slug', 'created', 'modified', 'average_rate')
    filter_horizontal = ( )
    list_filter = ('created',)
    inlines = [ProductImageInline]
    fieldsets_with_inlines = (
        ("Product Head", {'fields': ('title', 'category',)}),
        ("Prodcut Base Image", {'fields': ('image',)}),
        (ProductImageInline),
        ("Product Details", {
         'fields': ('price', 'discount_price', 'description', 'additional_info', 'average_rate')}),
        ("Product Permission/Others",
         {'fields': ('status','slug', 'featured', 'created', 'modified')}),
    )
         

class CategroyAdmin(DraggableMPTTAdmin):
    model = Category
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'title', 'parent', 'slug',
                    'related_products_count', 'related_products_cumulative_count',)
    list_display_links = ('indented_title', 'parent', 'slug')
    search_fields = ('title', 'parent__title', 'slug')
    readonly_fields = ('slug', 'created', 'updated')
    filter_horizontal = ()
    list_filter = ('parent',)
    fieldsets = (
        ("Category Details", {
         'fields': ('title', 'parent', 'image', 'slug', 'created', 'updated')}),
    )

    def get_queryset(self, request):
        query = super(CategroyAdmin, self).get_queryset(request)

        query = Category.objects.add_related_count(
            query,
            Products,
            'category',
            'products_cumulative_count',
            cumulative=True)
        query = Category.objects.add_related_count(
            query,
            Products,
            'category',
            'products_count',
            cumulative=False)
        return query

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Products (In This catgory)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Products (In This Tree)'


@admin_thumbnails.thumbnail('images')
class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ['images', 'product_slug',
                    'short_description', 'images_thumbnail']

    def product_slug(self, instance):
        return instance.product.slug
    product_slug.short_description = "Product Slug"
    product_slug.admin_order_field = "product__slug"


admin.site.register(Review)
admin.site.register(Image, ImageAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Category, CategroyAdmin)
