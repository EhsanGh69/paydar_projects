from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import Q

from django_jalali.db import models as jmodels
from jalali_date import datetime2jalali



class UserManager(BaseUserManager):
    def search(self, query):
        lookup = (
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()
    
    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create( # type: ignore
            username, # type: ignore
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    mobile_number = models.CharField(max_length=20, unique=True, default="بدون شماره", verbose_name="شماره همراه")

    objects = UserManager() # type: ignore

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def jalali_date_joined(self):
        return datetime2jalali(self.date_joined).strftime('%Y/%m/%d _ %H:%M:%S') # type: ignore
    
    def jalali_last_login(self):
        return datetime2jalali(self.last_login).strftime('%Y/%m/%d _ %H:%M:%S')  # type: ignore
    

class UserActionsLog(models.Model):
    LOG_TYPE = [
        ("CR", "Create Object"),
        ("UP", "Update Object"),
        ("DL", "Delete Object"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_logs')
    log_type = models.CharField(max_length=2, choices=LOG_TYPE)
    log_content = models.CharField(max_length=250)
    log_time = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}-{self.log_content}'
    