from django import forms
from django.core import validators


from .models import Receive, Organization, Payment, Activity
from utils.tools import none_numeric_value




class ReceiveForm(forms.ModelForm):
    use_required_attribute = False
    class Meta:
        model = Receive
        fields = ['organization', 'receive_for', 'project', 'receive_amount', 'receive_date']


    def __init__(self, *args, **kwargs):
        super(ReceiveForm, self).__init__(*args, **kwargs)

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


class PaymentForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Payment
        fields = ['organization', 'payment_for', 'project', 'payment_amount', 'payment_date']


    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

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


class ActivityForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Activity
        fields = ['organization', 'activity_type', 'project', 'activity_date',
                  'activity_result', 'activity_descriptions']


    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)

        self.fields['activity_type'] = forms.CharField(
            label="نوع فعالیت",
            validators=[none_numeric_value]
        )