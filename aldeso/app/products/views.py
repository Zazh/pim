# views.py
from rest_framework import filters, viewsets

from products.services import StandardResultsSetPagination
from .models import Product, ProductCategory
from .serializers import ProductSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Product.objects
        .select_related("category")
        .prefetch_related(
            "images",                     # галерея
            "attribute_values__attribute" # ← правильный путь
        )
    )
    serializer_class = ProductSerializer
    filter_backends   = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # ➊ Фильтры django-filter
    filterset_fields = {
        # категория (по slug, а не по id, удобнее во фронте)
        "category__slug": ["exact"],

        # ценовой диапазон
        "price": ["gte", "lte"],

        # атрибуты: slug атрибута + значение
        "attribute_values__attribute__slug": ["exact"],
        "attribute_values__value":           ["exact", "icontains"],
    }

    # ➋ Полнотекстовый поиск
    search_fields = ["title", "description", "sku"]

    # ➌ Сортировка
    ordering_fields = ["price", "title"]

    # ➍ Стандартная пагинация (если нужна)
    pagination_class = StandardResultsSetPagination



class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
