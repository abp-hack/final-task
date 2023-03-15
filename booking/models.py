from django.db import models
from application.models import HotelNumber, Hotel
from django.db.models import Q
from django.core.exceptions import ValidationError
import datetime


class Booking(models.Model):
    date_started = models.DateField('Дата начала', null=True, blank=True)
    date_end = models.DateField('Дата окончания', null=True, blank=True)
    date_len = models.PositiveIntegerField('Сколько ночей', blank=True, null=True)
    number = models.ForeignKey(HotelNumber, verbose_name='Номер отеля', on_delete=models.CASCADE, blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель', null=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def clean(self):
        if self.date_end is None and self.date_len is None:
            raise ValidationError("Укажите конечную дату либо количество ночей")
        if self.date_end is not None:
            self.date_len = (self.date_end - self.date_started).days
        if self.date_len:
            self.date_end = self.date_started + datetime.timedelta(days=self.date_len)

        numbers = HotelNumber.objects.filter(hotel=self.hotel)

        bookings = Booking.objects.filter(
            (
                Q(date_started__lte=self.date_started) &
                Q(date_end__gt=self.date_started) &
                Q(date_end__gte=self.date_end) &
                Q(date_started__lt=self.date_end)
            ) | (
                Q(date_started__gte=self.date_started) &
                Q(date_end__gt=self.date_started) &
                Q(date_end__gte=self.date_end) &
                Q(date_started__lt=self.date_end)
            ) | (
                Q(date_started__lte=self.date_started) &
                Q(date_end__gt=self.date_started) &
                Q(date_end__lte=self.date_end) &
                Q(date_started__lt=self.date_end)
            ) | (
                Q(date_started__gte=self.date_started) &
                Q(date_end__gt=self.date_started) &
                Q(date_end__lte=self.date_end) &
                Q(date_started__lt=self.date_end)
            )
        )
        bookings = list(filter(lambda x: x.id != self.id, bookings))
        #raise ValidationError(f'На такие даты уже есть номера {", ".join(map(str, bookings))}')
        booked_numbers = list(map(lambda x: x.number, bookings))
        num = None
        for number in numbers:
            if number not in booked_numbers:
                num = number
                break
        if not num:
            raise ValidationError(f'На такие даты свободных номеров не найдено')
        else:
            self.number = num
    
    def __str__(self):
        return f'{self.date_started.strftime("%m.%d.%Y")} - {self.date_end.strftime("%m.%d.%Y")}'
