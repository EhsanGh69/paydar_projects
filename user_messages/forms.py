from django import forms
from django.core import validators

from account.models import User


class MessageForm(forms.Form):
    use_required_attribute = False
    self_user = kwargs.pop('user')
    FULL_NAMES = [(user.id, user.get_full_name()) for user in User.objects.all() if user != self_user]
    receiver_name = forms.ChoiceField(
        widget=forms.Select(),
        choices=FULL_NAMES,
        label='گیرنده پیام',
        required=True
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
    