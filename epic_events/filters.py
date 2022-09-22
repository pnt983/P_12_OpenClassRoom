from django_filters import rest_framework as filters

from .models import Customer, Contract, Event


class CustomerFilters(filters.FilterSet):

    company_name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['company_name', 'email']


class ContractFilters(filters.FilterSet):

    company_name = filters.CharFilter(field_name='client', lookup_expr='company_name__icontains')
    customer_email = filters.CharFilter(field_name='client', lookup_expr='email__icontains')
    amount = filters.NumberFilter()
    date_created = filters.DateFilter(lookup_expr='icontains')

    class Meta:
        model = Contract
        fields = ['company_name', 'customer_email', 'amount', 'date_created']


class EventFilters(filters.FilterSet):

    company_name = filters.CharFilter(field_name='client', lookup_expr='company_name__icontains')
    customer_email = filters.CharFilter(field_name='client', lookup_expr='email__icontains')
    event_date = filters.DateFilter(lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['company_name', 'customer_email', 'event_date']

