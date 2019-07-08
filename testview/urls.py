from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('foo/', include('foo.urls', namespace='foo')),
    path('accounts/', include('django.contrib.auth.urls')),
]
