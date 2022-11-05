from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title

from .permissions import AdminOrReadOnly


class CategoriesGenresViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    pagination_class = LimitOffsetPagination
    lookup_field = "slug"


class TitleFilter(filters.FilterSet):
    """Класс для фильтрации произвелений."""
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='iexact')
    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact'
    )
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year')
