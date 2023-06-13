from django import forms
from django.core import validators

from jalali_date.fields import JalaliDateTimeField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
import django_jalali.admin as jadmin


from .models import Owners
from utils.tools import none_numeric_value



class OwnerCreateForm(forms.ModelForm):
    use_required_attribute = False
    class Meta:
        model = Owners
        fields = ['full_name', 'phone', 'national_card_image', 'birth_certificate_image', 'ownership_document_image']

    def __init__(self, *args, **kwargs):
        super(OwnerCreateForm, self).__init__(*args, **kwargs)

        self.fields['full_name'] = forms.CharField(
            label="نام و نام خانوادگی",
            validators=[none_numeric_value]
        )

        self.fields['phone'] = forms.CharField(
            label="شماره تماس",
            validators=[
                validators.RegexValidator(
                    regex=r'^0\d{10}$',
                    message="شماره تماس وارد شده معتبر نمی‌باشد"
                )
            ]
        )

        









