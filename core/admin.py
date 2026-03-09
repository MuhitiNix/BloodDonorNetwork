from django.contrib.gis import admin
from .models import DonorProfile

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.GISModelAdmin):
    
    list_display = ('user', 'blood_group', 'phone_number', 'last_donation_date')
    
    
    search_fields = ('phone_number', 'blood_group', 'user__first_name')
    
    list_filter = ('blood_group', 'is_available')