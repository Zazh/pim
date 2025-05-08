from rest_framework import serializers
from .models import (
    Product, ProductCategory,
    ProductImage, ProductAttributeValue
)

class ProductImageSerializer(serializers.ModelSerializer):
    default_url = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "default_url", "preview_url", "is_main"]

    def _abs(self, url):
        req = self.context.get("request")
        return req.build_absolute_uri(url) if req else url

    def get_default_url(self, obj):
        return self._abs(obj.thumb("default"))

    def get_preview_url(self, obj):
        return self._abs(obj.thumb("preview"))

class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(source="attribute.name")  # ← было attribute_value.attribute.label
    value     = serializers.CharField()

    class Meta:
        model  = ProductAttributeValue
        fields = ["attribute", "value"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    attributes = ProductAttributeValueSerializer(source="attribute_values", many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "title", "sku", "slug", "description", "price", "category", "images", "attributes"]

    def get_category(self, obj):
        if obj.category:
            return {"id": obj.category.id, "title": obj.category.title}
        return None

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "title", "parent_id"]
