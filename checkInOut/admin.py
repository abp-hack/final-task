from django.contrib import admin
from .models import CheckIn, CheckOut, CheckGuest, CheckinWithoutBooking
from application.models import HotelNumber, Status

from booking.models import Client, Guest, Payment
from dynamic_admin_forms.admin import DynamicModelAdminMixin
from django.db.models import Q


admin.site.register(Status)
class GuestStacked(admin.StackedInline):
    model = CheckGuest
    fields = ('guest',)
    extra = 0

@admin.register(CheckIn)
class CheckInAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    class Meta:
        model = CheckIn
    fields = ('date_start', 'hotel', 'booking', 'number', 'date_end')
    dynamic_fields = ('number', )
    inlines = (GuestStacked, )

    def get_dynamic_number_field(self, data):
        q = HotelNumber.objects.filter(Q(
            status__text='Свободен (чистый)'
    ) | Q(status__text='Свободен (грязный)'))
        if 'hotel' in data.keys():
            q = q.filter(hotel=data['hotel'])
        return q, data['number'], False

@admin.register(CheckOut)
class CheckOutAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    class Meta:
        model = CheckOut

    fields = ('date', 'hotel', 'number')
    dynamic_fields = ('number', )
    inlines = (GuestStacked, )

    print(list(HotelNumber.objects.all()))

    def get_dynamic_number_field(self, data):
        q = HotelNumber.objects.filter(Q(
            status__text='Занят'
    ) | Q(status__text='Заняты (грязный)'))
        if 'hotel' in data.keys():
            q = q.filter(hotel=data['hotel'])
        return q, data['number'], False


admin.site.register(CheckinWithoutBooking)