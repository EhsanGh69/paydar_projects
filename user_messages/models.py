from django.db import models
from django.db.models.query import Q

from account.models import User



class MessageManager(models.Manager):
    def search(self, query):
        lookup = (
            Q(sender__first_name__icontains=query) |
            Q(receiver__first_name__icontains=query) |
            Q(sender__last_name__icontains=query) |
            Q(receiver__last_name__icontains=query) |
            Q(subject__icontains=query) |
            Q(content__icontains=query) 
        )
        return self.get_queryset().filter(lookup).distinct()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_users', verbose_name='فرستنده پیام')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_users', verbose_name='دریافت‌ کننده پیام')
    subject = models.CharField(max_length=150, verbose_name='موضوع پیام')
    content = models.TextField(verbose_name='متن پیام')
    date_time = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False, verbose_name="خوانده شده")
    archive_sender = models.BooleanField(default=False)
    archive_receiver = models.BooleanField(default=False)
    visible_sender = models.BooleanField(default=True)
    visible_receiver = models.BooleanField(default=True)

    objects = MessageManager()

    class Meta:
        permissions = (
            ("write_message", "نوشتن پیام"),
            ("seen_message", "مشاهده پیام")
        )

    def __str__(self):
        return f'از: {self.sender} - به: {self.receiver} - موضوع: {self.subject}'
