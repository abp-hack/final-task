from django.contrib import admin
from .models import Booking
from django.db.models import Q
from django.core.exceptions import ValidationError

# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     class Meta:
#         model = Booking
#     fields = ('date_started', 'date_end', 'date_len', 'hotel')
