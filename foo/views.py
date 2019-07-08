from tools.generic_views import *
from foo.models import Foo, Bar, Multibar
from django.utils.translation import gettext as _


class FooCreateView(GenericCreateView):
    model = Foo


class BarCreateView(GenericCreateView):
    model = Bar


class MultibarCreateView(GenericCreateView):
    model = Multibar


class FooListView(GenericListView):
    model = Foo


class BarListView(GenericListView):
    model = Bar


class MultibarListView(GenericListView):
    model = Multibar


class FooUpdateView(GenericUpdateView):
    model = Foo


class BarUpdateView(GenericUpdateView):
    model = Bar


class MultibarUpdateView(GenericUpdateView):
    model = Multibar


class FooDetailView(GenericDetailView):
    model = Foo


class BarDetailView(GenericDetailView):
    model = Bar


class MultibarDetailView(GenericDetailView):
    model = Multibar


class FooDeleteView(GenericDeleteView):
    model = Foo


class MultibarDeleteView(GenericDeleteView):
    model = Multibar
