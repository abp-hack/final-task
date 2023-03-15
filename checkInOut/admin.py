from django.contrib import admin
from .models import CheckIn, CheckOut, TodayNumbers, TodayLogoutNumbers, EmptyModel
from application.models import HotelNumber
import datetime
from booking.models import Booking

admin.site.register(CheckOut)
admin.site.register(CheckIn)

@admin.action(description='Оформить заезд')
def get_check_in(modeladmin, request, queryset):
    pass

@admin.action(description='Оформить выезд')
def get_check_out(modeladmin, request, queryset):
    pass

@admin.register(TodayNumbers)
class EmptyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Booking.objects.filter(date_started=datetime.datetime.now().date())
    actions = [get_check_in]
    class Meta:
        model = TodayNumbers


@admin.register(TodayLogoutNumbers)
class EmptyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Booking.objects.filter(date_end=datetime.datetime.now().date())
    actions = [get_check_out]
    class Meta:
        model = TodayLogoutNumbers

@admin.register(EmptyModel)
class EmptyModelAdmin(admin.ModelAdmin):
    change_list_template = 'screen.html'
    class Meta:
        model = EmptyModel