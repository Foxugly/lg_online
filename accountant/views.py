from accountant.models import Accountant
from tools.generic_views import *


class ContactCreateView(GenericCreateView):
    model = Accountant


class ContactListView(GenericListView):
    model = Accountant


class ContactUpdateView(GenericUpdateView):
    model = Accountant


class ContactDetailView(GenericDetailView):
    model = Accountant


class ContactDeleteView(GenericDeleteView):
    model = Accountant
