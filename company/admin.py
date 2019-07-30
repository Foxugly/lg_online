from django.contrib import admin
from company.models import Company, Iban
# Register your models here.


class IbanAdmin(admin.ModelAdmin):
    pass


class IbanInline(admin.StackedInline):
    model = Iban
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    inlines = [IbanInline]


admin.site.register(Iban, IbanAdmin)
admin.site.register(Company, CompanyAdmin)
