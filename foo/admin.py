from django.contrib import admin
from foo.models import Bar, Multibar, Foo
# Register your models here.


class BarAdmin(admin.ModelAdmin):
    pass


class MultibarAdmin(admin.ModelAdmin):
    pass


class FooAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bar, BarAdmin)
admin.site.register(Multibar, MultibarAdmin)
admin.site.register(Foo, FooAdmin)
