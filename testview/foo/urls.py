from django.urls import path, include
from foo.views import FooListView, FooUpdateView, FooDetailView, FooCreateView, FooDeleteView

app_name = 'foo'
urlpatterns = [
    path('foo/', FooListView.as_view(), name='foo_list'),
    path('foo/add/', FooCreateView.as_view(), name="foo_add"),
    path('foo/<int:pk>/change/', FooUpdateView.as_view(), name="foo_change"),
    path('foo/<int:pk>/', FooDetailView.as_view(), name="foo_detail"),
    path('foo/<int:pk>/delete', FooDeleteView.as_view(), name="foo_delete"),
]
