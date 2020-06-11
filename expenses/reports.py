from collections import OrderedDict
from .models import Expense
from django.db.models import Sum, Value, Count
from django.db.models.functions import TruncMonth
from django.db.models.functions import Coalesce


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def summary_per_year_month(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(
            year_month=TruncMonth('date'),
        )
        .order_by()
        .values('year_month')
        .annotate(sum=Sum('amount'))
        .values_list('year_month', 'sum')
    ))


def overall_summary(queryset):
    sum = queryset.aggregate(Sum('amount'))['amount__sum']

    return sum