from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import Q

from jalali_date import datetime2jalali



class UserManager(BaseUserManager):
    def search(self, query):
        lookup = (
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class User(AbstractUser):
    mobile_number = models.CharField(max_length=20, unique=True, default="بدون شماره", verbose_name="شماره همراه")

    objects = UserManager()

    def jalali_date_joined(self):
        return datetime2jalali(self.date_joined).strftime('%Y/%m/%d _ %H:%M:%S')
    
    def jalali_last_login(self):
        return datetime2jalali(self.last_login).strftime('%Y/%m/%d _ %H:%M:%S')

