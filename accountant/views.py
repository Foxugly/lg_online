from tools.generic_views import *
from accountant.models import Accountant


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
