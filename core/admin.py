from django.contrib import admin # type: ignore
from .models import Scheme, Exam, TaxUpdate, UserExtendedProfile  # Updated import

@admin.register(UserExtendedProfile)
class UserExtendedProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_name', 'middle_name', 'last_name', 'father_name', 'mother_name',
        'dob', 'marital_status', 'urban_rural', 'religion', 'category', 'disability',
        'ex_serviceman', 'priority_ex_service', 'eyesight', 'chest', 'height',
        'weight', 'address', 'pin', 'locality', 'mobile', 'email', 'tel'
    )
    search_fields = ('user__username', 'first_name', 'last_name', 'mobile', 'email')
    list_filter = ('category', 'religion', 'urban_rural', 'disability', 'ex_serviceman')
    ordering = ('user',)

# Register other models
admin.site.register(Scheme)
admin.site.register(Exam)
admin.site.register(TaxUpdate)
