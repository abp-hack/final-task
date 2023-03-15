from django.db import models
from booking.models import Booking
from application.models import HotelNumber, Status
# Create your models here.

class CheckIn(models.Model): #заселение только по предварительному бронированию
    class Meta():
        verbose_name='Заезд'
        verbose_name_plural='Заезды'
    
    date = models.DateField('Дата заезда')
    client = models.CharField(verbose_name='ИМЯ заезжающего', max_length=50) #исправить на foreignKey на модель заезжающего с паспортом и тд
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name='Бронирование', unique=True)
    # room = models.ForeignKey(HotelNumber,on_delete=models.CASCADE,  verbose_name='Номер в отеле (комната)')
    def __str__(self):
        return f'Заезд {self.date}, {self.client}'
    
    def save(self,*args, **kwargs):
        self.booking.number.status = Status.objects.filter(text='Занято')[0]
        self.booking.number.save()
        super(CheckIn, self).save(*args, **kwargs)

class CheckOut(models.Model): #заселение только по предварительному бронированию
    class Meta():
        verbose_name='Выезд'
        verbose_name_plural='Выезды'
    
    date = models.DateField('Дата выезда')
    checkin = models.ForeignKey(CheckIn, on_delete=models.CASCADE, verbose_name='Заезд', unique=True)
    # room = models.ForeignKey(HotelNumber,on_delete=models.CASCADE,  verbose_name='Номер в отеле (комната)')
    def __str__(self):
        return f'Выезд {self.date},  {self.checkin.client}'
    
    def save(self,*args, **kwargs):
        self.checkin.booking.number.status = Status.objects.filter(text='Требует уборки')[0]
        self.checkin.booking.number.save()
        super(CheckOut, self).save(*args, **kwargs)


class TodayNumbers(Booking):
    class Meta:
        proxy = True
        verbose_name = 'Номера для заезда сегодня'
        verbose_name_plural = 'Номера для заезда сегодня'

class TodayLogoutNumbers(Booking):
    class Meta:
        proxy = True
        verbose_name = 'Номера для выезда сегодня'
        verbose_name_plural = 'Номера для выезда сегодня'

class EmptyModel(models.Model):
    class Meta:
        verbose_name = 'Рабочий стол'
        verbose_name_plural = 'Рабочий стол'