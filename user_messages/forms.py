from django import forms
from django.core import validators

from account.models import User


class MessageForm(forms.Form):
    use_required_attribute = False
    
    receiver_name = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(),
        label='گیرنده پیام',
        required=False
    )

    subject = forms.CharField(
        widget=forms.TextInput(),
        required=True,
        label="موضوع پیام",
        validators=[
            validators.MaxLengthValidator(
                limit_value=150,
                message="موضوع پیام حداکثر ۱۵۰ کاراکتر می تواند باشد"
            )
        ]
    )

    content = forms.CharField(
        widget=forms.Textarea(),
        required=True,
        label="متن پیام"
    )
    