from django.contrib import admin
from .models import Booking
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Client, Guest, Payment
from dynamic_admin_forms.admin import DynamicModelAdminMixin
from dynamic_admin_forms.admin import DynamicModelAdminMixin
from application.models import HotelNumber

class GuestTabular(admin.TabularInline):
    model = Guest
    extra = 0


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


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    class Meta:
        model = Payment


@admin.register(Booking)
class BookingAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    class Meta:
        model = Booking
    fields = ('date_started', 'date_end', 'hotel', 'number', 'cost', 'payer', 'checked')
    dynamic_fields = ('number', )
    inlines = (GuestTabular, )

    def get_dynamic_number_field(self, data):
        q = HotelNumber.objects.all()
        if 'hotel' in data.keys():
            q = q.filter(hotel=data['hotel'])
        return HotelNumber.objects.filter(hotel=data['hotel']), data['number'], False
