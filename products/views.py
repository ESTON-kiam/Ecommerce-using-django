from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().filter(available=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category_slug'] = self.kwargs.get('category_slug')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        """Verify user is not a customer."""
        return not getattr(self.request.user, 'is_customer', True)

    def handle_no_permission(self):
        """Redirect to login page if not authenticated, or home if unauthorized."""
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('login') + f'?next={self.request.path}')
        return redirect('product_list')

    def form_valid(self, form):
        """Set the product's added_by field to the current user."""
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    slug_url_kwarg = 'slug'

    def test_func(self):
        """Verify user is not a customer."""
        return not getattr(self.request.user, 'is_customer', True)

    def handle_no_permission(self):
        """Redirect to login page if not authenticated, or home if unauthorized."""
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('login') + f'?next={self.request.path}')
        return redirect('product_list')

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'slug': self.object.slug})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        """Verify user is not a customer."""
        return not getattr(self.request.user, 'is_customer', True)

    def handle_no_permission(self):
        """Redirect to login page if not authenticated, or home if unauthorized."""
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('login') + f'?next={self.request.path}')
        return redirect('product_list')