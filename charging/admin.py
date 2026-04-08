
from django.contrib import admin
from .models import EVAdmin, EVRegister, EVStation, EVBooking

admin.site.register(EVAdmin)

@admin.register(EVRegister)
class EVRegisterAdmin(admin.ModelAdmin):
    fields = ('uname', 'name', 'address', 'mobile', 'email', 'passw')
    list_display = ('uname', 'name', 'email', 'mobile')

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'show_save_and_add_another': False, 'show_save_and_continue': False})
        return super().changeform_view(request, object_id, form_url, extra_context)

admin.site.register(EVStation)
admin.site.register(EVBooking)
