from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, FormView, ListView, DetailView, DeleteView
from foo.models import Foo
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from view_breadcrumbs import ListBreadcrumbMixin, UpdateBreadcrumbMixin, DetailBreadcrumbMixin, CreateBreadcrumbMixin


class FooCreateView(CreateBreadcrumbMixin, CreateView):
    model = Foo
    fields = '__all__'
    template_name = 'update.html'
    success_url = reverse_lazy('foo:foo_list')


class FooListView(ListBreadcrumbMixin, ListView):
    model = Foo
    paginate_by = 10
    ordering = ['pk']
    template_name = 'list.html'
    success_url = reverse_lazy('foo:foo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        return context


class FooUpdateView(UpdateBreadcrumbMixin, UpdateView):
    model = Foo
    fields = '__all__'
    template_name = 'update.html'
    success_url = reverse_lazy('foo:foo_list')

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        return context


class FooDetailView(DetailBreadcrumbMixin, DetailView):
    model = Foo
    template_name = 'detail.html'


class FooDeleteView(DeleteView):
    model = Foo

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('foo:foo_list')
