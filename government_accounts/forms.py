from django import forms
from django.core import validators
from jalali_date.fields import JalaliDateTimeField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
import django_jalali.admin as jadmin

from .models import Receive, Organization, Payment, Activity
from utils.tools import none_numeric_value




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


class OrganizationForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Organization
        fields = ["organization_name"]

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)

        self.fields['organization_name'] = forms.CharField(
            label="نام ارگان",
            validators=[
                none_numeric_value,
                validators.MaxLengthValidator(
                    limit_value=50,
                    message="تعداد کاراکترهای وارد شده نمی‌تواند بیشتر از ۵۰ باشد"
                )
            ]
        )


class PaymentCreateForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Payment
        fields = ['organization', 'payment_for', 'project', 'payment_amount', 'payment_date']


    def __init__(self, *args, **kwargs):
        super(PaymentCreateForm, self).__init__(*args, **kwargs)

        self.fields['payment_amount'] = forms.IntegerField(
            label="مبلغ پرداختی",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار مبلغ پرداختی نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['payment_for'] = forms.CharField(
            label="پرداخت بابت",
            validators=[none_numeric_value]
        )

        self.fields['payment_date'] = JalaliDateTimeField(
            label='تاریخ و زمان پرداخت',
            widget=AdminJalaliDateWidget
        )

        self.fields['payment_date'] = SplitJalaliDateTimeField(
            label='تاریخ و زمان پرداخت',                                           
            widget=AdminSplitJalaliDateTime
        )


class PaymentUpdateForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Payment
        fields = ['organization', 'payment_for', 'project', 'payment_amount', 'payment_date']


    def __init__(self, *args, **kwargs):
        super(PaymentUpdateForm, self).__init__(*args, **kwargs)

        self.fields['payment_amount'] = forms.IntegerField(
            label="مبلغ پرداختی",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار مبلغ پرداختی نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['payment_for'] = forms.CharField(
            label="پرداخت بابت",
            validators=[none_numeric_value]
        )


class ActivityCreateForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Activity
        fields = ['organization', 'activity_type', 'project', 'activity_date',
                  'activity_result', 'activity_descriptions']


    def __init__(self, *args, **kwargs):
        super(ActivityCreateForm, self).__init__(*args, **kwargs)


        self.fields['activity_type'] = forms.CharField(
            label="نوع فعالیت",
            validators=[none_numeric_value]
        )

        self.fields['activity_date'] = JalaliDateTimeField(
            label='تاریخ و زمان فعالیت',
            widget=AdminJalaliDateWidget
        )

        self.fields['activity_date'] = SplitJalaliDateTimeField(
            label='تاریخ و زمان فعالیت',                                           
            widget=AdminSplitJalaliDateTime
        )


class ActivityUpdateForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Activity
        fields = ['organization', 'activity_type', 'project', 'activity_date',
                  'activity_result', 'activity_descriptions']


    def __init__(self, *args, **kwargs):
        super(ActivityUpdateForm, self).__init__(*args, **kwargs)


        self.fields['activity_type'] = forms.CharField(
            label="نوع فعالیت",
            validators=[none_numeric_value]
        )





