from tools.generic_urls import add_url_from_generic_views


app_name = 'company'
urlpatterns = add_url_from_generic_views('company.views')