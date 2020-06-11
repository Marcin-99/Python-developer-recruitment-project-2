from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import path, reverse_lazy
from .models import Expense, Category
from .views import ExpenseListView,\
                   CategoryListView,\
                   CreateCategoryView,\
                   UpdateCategoryView, \
                   DeleteCategoryView, \
                   CategoryDetailView


urlpatterns = [
    path('expense/list/',
         ExpenseListView.as_view(),
         name='expense-list'),
    path('expense/create/',
         CreateView.as_view(
            model=Expense,
            fields='__all__',
            success_url=reverse_lazy('expenses:expense-list')
         ),
         name='expense-create'),
    path('expense/<int:pk>/edit/',
         UpdateView.as_view(
            model=Expense,
            fields='__all__',
            success_url=reverse_lazy('expenses:expense-list')
         ),
         name='expense-edit'),
    path('expense/<int:pk>/delete/',
         DeleteView.as_view(
             model=Expense,
             success_url=reverse_lazy('expenses:expense-list')
         ),
         name='expense-delete'),

    path('categories/list/',
         CategoryListView.as_view(),
         name='categories-list'),
    path('categories/create/',
         CreateCategoryView.as_view(),
         name='categories-create'),
    path('categories/<int:pk>/edit/',
         UpdateCategoryView.as_view(),
         name='category-edit'),
    path('categories/<int:pk>/delete/',
         DeleteCategoryView.as_view(),
         name='category-delete'),
    path('categories/<int:pk>/details/',
         CategoryDetailView.as_view(),
         name='category-details'),
]