import django_filters
from .models import Income, Expence
from datetime import datetime

class IncomeFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="time", lookup_expr='gte', label='Start Date')
    end_date = django_filters.DateFilter(field_name="time", lookup_expr='lte', label='End Date')

    class Meta:
        model = Income
        fields = ['start_date', 'end_date']

class ExpenceFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="time", lookup_expr='gte', label='Start Date')
    end_date = django_filters.DateFilter(field_name="time", lookup_expr='lte', label='End Date')

    class Meta:
        model = Expence
        fields = ['start_date', 'end_date']
