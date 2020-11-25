from django.contrib import admin

from company.models import Company, Iban


class IbanInline(admin.StackedInline):
    model = Iban
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['enterprise_number', 'enterprise_status', 'legal_situation',
                           'start_date', 'enterprise_name',
                           'legal_form', 'end_fiscal_date']}),
        ('address', {'fields': ['social_address_street',
                                'social_address_number', 'social_address_zip',
                                'social_address_city', 'social_address_country']}),
        ('proposal',
         {'fields': ['calculated_amount', 'date_calculated_amount', 'proposed_amount', 'date_proposed_amount']}),
        ('validation',
         {'fields': ['accountant', 'valid', 'valid_user', 'sent', 'active', 'token', 'subscription_status']})
    ]
    inlines = [IbanInline]


admin.site.register(Company, CompanyAdmin)
