from django.contrib import admin
from company.models import Company
# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
