from django.contrib import admin
from .models import Booking
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Client, Guest
from dynamic_admin_forms.admin import DynamicModelAdminMixin

@admin.register(Guest)
class GuestAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
     mask = {
         'tel': '+7(900)000-00-00'
        }
admin.site.register(Client)          
# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     class Meta:
#         model = Booking
#     fields = ('date_started', 'date_end', 'date_len', 'hotel')
