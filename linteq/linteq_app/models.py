import datetime
from datetime import timedelta

from django.db import models
from django.utils import timezone


class Consultation(models.Model):

    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=255, verbose_name='Тема')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    message = models.TextField(default=None, verbose_name='Сопроводительное письмо')

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Заявки"

    def __str__(self):
        return self.name


class FileData(models.Model):
    path = models.CharField(max_length=255, verbose_name='адрес')
    create_date = models.DateTimeField(auto_now_add=True)
    delete_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=1))

    class Meta:
        ordering = ['-create_date']
        verbose_name_plural = 'События'
