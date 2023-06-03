from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from jalali_date.fields import JalaliDateTimeField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
import django_jalali.admin as jadmin

from .models import Receive



def none_numeric_value(value):
    try:
        is_numeric = type(int(value)) is int
    except Exception:
        return True
    
    if is_numeric :
            raise ValidationError("مقدار این فیلد نمی‌تواند عددی می‌باشد", params={"value": value})



class ReceiveCreateForm(forms.ModelForm):
    use_required_attribute = False
    class Meta:
        model = Receive
        fields = ['organization', 'receive_for', 'project', 'receive_amount', 'receive_date']


    def __init__(self, *args, **kwargs):
        super(ReceiveCreateForm, self).__init__(*args, **kwargs)

        self.fields['receive_amount'] = forms.IntegerField(
            label="مبلغ دریافتی",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار مبلغ دریافتی نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['receive_for'] = forms.CharField(
            label="دریافت بابت",
            validators=[none_numeric_value]
        )

        self.fields['receive_date'] = JalaliDateTimeField(
            label='تاریخ و زمان دریافت',
            widget=AdminJalaliDateWidget
        )

        self.fields['receive_date'] = SplitJalaliDateTimeField(
            label='تاریخ و زمان دریافت',                                           
            widget=AdminSplitJalaliDateTime
        )


class ReceiveUpdateForm(forms.ModelForm):
    use_required_attribute = False
    class Meta:
        model = Receive
        fields = ['organization', 'receive_for', 'project', 'receive_amount', 'receive_date']


    def __init__(self, *args, **kwargs):
        super(ReceiveUpdateForm, self).__init__(*args, **kwargs)

        self.fields['receive_amount'] = forms.IntegerField(
            label="مبلغ دریافتی",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار مبلغ دریافتی نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['receive_for'] = forms.CharField(
            label="دریافت بابت",
            validators=[none_numeric_value]
        )