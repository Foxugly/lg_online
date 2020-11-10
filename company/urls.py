from django.urls import path

from company.proposal_views import CompanyProposalUpdateView, CompanyProposalListView, send_proposal, confirm_proposal, \
    CompanyProposalPdfView, run_config
from tools.generic_urls import add_url_from_generic_views

app_name = 'company'
urlpatterns = [
                  path('proposal/', CompanyProposalListView.as_view(), name='company_proposal_list'),
                  path('proposal/<int:pk>/change/', CompanyProposalUpdateView.as_view(),
                       name='company_proposal_change'),
                  path('proposal/<int:pk>/send/', send_proposal, name='company_proposal_send'),
                  path('proposal/<int:pk>/confirm/<str:uidb64>/<str:token>/', confirm_proposal,
                       name='confirm_proposal'),
                  path('proposal/<int:pk>/pdf/<str:token>/', CompanyProposalPdfView.as_view(),
                       name='company_proposal_pdf'),
                  path('go/<int:pk>/', run_config, name='company_go'),

              ] + add_url_from_generic_views('company.views')
