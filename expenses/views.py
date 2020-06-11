from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month, overall_summary


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        queryset = Expense.objects.filter(category=self.object)

        return super().get_context_data(
            summary_per_year_month=summary_per_year_month(queryset),
            **kwargs
        )


class CreateCategoryView(SuccessMessageMixin, CreateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('expenses:categories-list')
    success_message = "%(name)s was created successfully."


class UpdateCategoryView(SuccessMessageMixin, UpdateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('expenses:categories-list')
    success_message = "%(name)s was updated successfully."


class DeleteCategoryView(DeleteView):
    model = Category
    success_url = reverse_lazy('expenses:categories-list')

    def get_context_data(self, **kwargs):
        queryset = Expense.objects.filter(category=self.object)
        expenses_summary = overall_summary(queryset)

        return super().get_context_data(
            summary=expenses_summary,
            **kwargs
        )


class CategoryListView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        categories_queryset = Category.objects.all()
        expenses_queryset = Expense.objects.all()

        paginate_by = self.request.GET.get('paginate', 5) or 5
        paginator = Paginator(categories_queryset, paginate_by)
        page = self.request.GET.get('page', 1)

        try:
            paginated = paginator.page(page)
        except PageNotAnInteger:
            paginated = paginator.page(1)
        except EmptyPage:
            paginated = paginator.page(paginator.num_pages)

        return super().get_context_data(
            objects=categories_queryset,
            paginated=paginated,
            paginate_by=paginate_by,
            paginator=paginator,
            summary_per_category=summary_per_category(expenses_queryset),
            **kwargs)


class ExpenseListView(ListView):
    model = Expense

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        form = ExpenseSearchForm(self.request.GET)

        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            if name:
                queryset = queryset.filter(name__icontains=name)

            grouping = form.cleaned_data['grouping']
            if grouping == 'date':
                queryset = queryset.order_by('date', '-pk')
            elif grouping == 'category':
                queryset = queryset.order_by('category', '-pk')

            min_date = form.cleaned_data['min_date']
            max_date = form.cleaned_data['max_date']
            if min_date and max_date:
                queryset = queryset.filter(date__range=[min_date, max_date])

            categories = form.cleaned_data['categories']
            if categories:
                categories_list = [Category.objects.get(name=category) for category in categories]
                queryset = Expense.objects.filter(category__in=categories_list)

            sort_by_date = form.cleaned_data['sort_by_date']
            if sort_by_date == "ascending":
                queryset = queryset.order_by('date')
            elif sort_by_date == "descending":
                queryset = queryset.order_by('-date')

            sort_by_category = form.cleaned_data['sort_by_category']
            if sort_by_category == "ascending":
                queryset = queryset.order_by('category')
            elif sort_by_category == "descending":
                queryset = queryset.order_by('-category')

        paginate_by = self.request.GET.get('paginate', 5) or 5
        paginator = Paginator(queryset, paginate_by)
        page = self.request.GET.get('page', 1)

        try:
            paginated = paginator.page(page)
        except PageNotAnInteger:
            paginated = paginator.page(1)
        except EmptyPage:
            paginated = paginator.page(paginator.num_pages)

        return super().get_context_data(
            form=form,
            objects=queryset,
            paginated=paginated,
            paginator=paginator,
            summary_per_category=summary_per_category(queryset),
            summary_per_year_month=summary_per_year_month(queryset),
            overall_summary = overall_summary(queryset),
            **kwargs)