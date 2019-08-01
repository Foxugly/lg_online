from tools.generic_views import *
from contact.models import Contact


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
