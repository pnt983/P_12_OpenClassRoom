from django_filters import rest_framework as filters

from .models import Customer, Contract, Event


class CustomerFilters(filters.FilterSet):

    # company_name = filters.CharFilter(lookup_expr='icontains')
    # email = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['company_name', 'email']
