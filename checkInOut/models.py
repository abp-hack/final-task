from django.db import models
from application.models import HotelNumber, Status, Hotel
# Create your models here.



class CheckIn(models.Model): #заселение только по предварительному бронированию
    class Meta():
        verbose_name='Заезд'
        verbose_name_plural='Заезды'
    
    date_start = models.DateField('Дата заезда')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель' )
    booking = models.ForeignKey('booking.Booking', on_delete=models.CASCADE, verbose_name='Бронирование', unique=True)
    number = models.ForeignKey(HotelNumber,on_delete=models.CASCADE,  verbose_name='Номер в отеле (комната)', blank=True, null=True)
    date_end = models.DateField('Дата выезда')

    def __str__(self):
            return f'Заезд {self.date}, {self.number}'

    def save(self,*args, **kwargs):
        hotel_number = self.booking.number
        hotel_number.status = Status.objects.get(text='Занят')
        hotel_number.date_started = self.booking.date_started
        hotel_number.date_end = self.booking.date_end
        hotel_number.save()
        super(CheckIn, self).save(*args, **kwargs)

class CheckOut(models.Model): #заселение только по предварительному бронированию
    class Meta():
        verbose_name='Выезд'
        verbose_name_plural='Выезды'
    
    date = models.DateField('Дата выезда')
    number = models.ForeignKey(HotelNumber,on_delete=models.CASCADE,  verbose_name='Освобождаемый номер', blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель' )

    # room = models.ForeignKey(HotelNumber,on_delete=models.CASCADE,  verbose_name='Номер в отеле (комната)')
    def __str__(self):
        return f'Выезд {self.date}'
    
    def save(self,*args, **kwargs):
        hotel_number = self.booking.number
        hotel_number.status = Status.objects.get(text='Свободен(грязный)')
        hotel_number.date_started = None
        hotel_number.date_end = None
        hotel_number.save()
        super(CheckOut, self).save(*args, **kwargs)

        
class CheckGuest(models.Model):
    class Meta():
        verbose_name='Заезжающий гость'
        verbose_name_plural='Заезжающие гости'
    
    guest = models.ForeignKey("booking.Guest", verbose_name='Гость', on_delete=models.CASCADE)
    checkIn = models.ForeignKey(CheckIn,  on_delete=models.CASCADE, null=True)
    checkOut = models.ForeignKey(CheckOut,  on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.guest