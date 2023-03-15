from django.contrib import admin
from .models import CheckIn, CheckOut
# Register your models here.
admin.site.register(CheckOut)
admin.site.register(CheckIn)
