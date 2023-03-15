from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    SEX_CHOICES = (
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский')
    )
    
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    mindame = models.CharField(max_length=100, verbose_name='Отчество')
    gender = models.CharField(choices=SEX_CHOICES, verbose_name='Пол', max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100, verbose_name='Пароль')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)



class SumModel(models.Model):
    email = models.CharField(max_length=100)
    sum = models.IntegerField()


class Sums(models.Model):
    field_a = models.IntegerField()
    field_b = models.IntegerField()
    model = models.ForeignKey(SumModel, on_delete=models.CASCADE)



class Hotel(models.Model):
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'
    
    name = models.CharField('Имя', max_length=100)

    def __str__(self):
        return f'Отель {self.name}'


class Status(models.Model):
    text = models.CharField(max_length=100, verbose_name='Текст')
    
    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class HotelNumber(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='numbers', verbose_name='Отель', on_delete=models.CASCADE)
    number = models.CharField('Номер', max_length=100)
    level = models.IntegerField('Этаж')
    status = models.ForeignKey(Status, related_name='numbers', verbose_name='Статус', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Номер отеля'
        verbose_name_plural = 'Номера отелей'
    
    def __str__(self):
        return f'Номер {self.hotel}'
