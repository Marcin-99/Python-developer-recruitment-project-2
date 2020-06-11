from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    choices = [[record.name, record.name] for record in Category.objects.all()]
    GROUPING = ('date', 'category')
    sorting = ('ascending', 'descending',)

    grouping = forms.ChoiceField(choices=[('', '')] + list(zip(GROUPING, GROUPING)))
    sort_by_date = forms.ChoiceField(choices=[('', '')] + list(zip(sorting, sorting)))
    sort_by_category = forms.ChoiceField(choices=[('', '')] + list(zip(sorting, sorting)))
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices)
    min_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput()
    )
    max_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput()
    )

    class Meta:
        model = Expense
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False