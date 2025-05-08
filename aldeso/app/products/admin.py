from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import (
    ProductCategory, Product, Attribute, AttributeValue,
    ProductImage, ProductAttributeValue
)

class ProductImageInline(ImageCroppingMixin, admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "cropping", "is_main", "thumbnail_preview")
    readonly_fields = ("thumbnail_preview",)

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 0
    autocomplete_fields = ["attribute"]

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "parent")
    search_fields = ("title",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "sku", "price")
    list_filter = ("category",)
    search_fields = ("title",)
    inlines = [ProductImageInline, ProductAttributeInline]

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    search_fields = ("label",)

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_select_related = ("attribute",)
    search_fields = ("value", "attribute__label")
