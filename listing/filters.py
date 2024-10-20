import django_filters
from .models import Property, Agent


class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    city = django_filters.CharFilter(lookup_expr='iexact')
    agent = django_filters.ModelChoiceFilter(queryset=Agent.objects.all())

    class Meta:
        model = Property
        fields = ['city', 'min_price', 'max_price', 'agent']
