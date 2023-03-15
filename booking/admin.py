from django.contrib import admin
from .models import Booking
from django.db.models import Q
from django.core.exceptions import ValidationError
from dynamic_admin_forms.admin import DynamicModelAdminMixin
from application.models import HotelNumber


@admin.register(Booking)
class BookingAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    class Meta:
        model = Booking
    fields = ('date_started', 'date_end', 'date_len', 'hotel', 'number', 'cost')
    dynamic_fields = ('number', )

    def get_dynamic_number_field(self, data):
        q = HotelNumber.objects.all()
        if 'hotel' in data.keys():
            q = q.filter(hotel=data['hotel'])
        return HotelNumber.objects.filter(hotel=data['hotel']), data['number'], False
