from tools.generic_views import *
from contact.models import Contact
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView


class ContactCreateView(GenericCreateView):
    model = Contact


class ContactListView(GenericListView):
    model = Contact


class ContactUpdateView(GenericUpdateView):
    model = Contact


class ContactDetailView(GenericDetailView):
    model = Contact


class ContactDeleteView(GenericDeleteView):
    model = Contact
