from tools.generic_urls import add_url_from_generic_views
from django.urls import path
from company.views import CompanyProposalUpdateView, CompanyProposalListView, send_proposal

app_name = 'company'
urlpatterns = [
    path('proposal/', CompanyProposalListView.as_view(), name='company_proposal_list'),
    path('proposal/<int:pk>/change/', CompanyProposalUpdateView.as_view(), name='company_proposal_change'),
    path('proposal/<int:pk>/send/', send_proposal, name='company_proposal_send'),

] + add_url_from_generic_views('company.views')
