from django import forms
from django.core import validators

from .models import Cheques
from utils.tools import none_numeric_value




class ChequesForm(forms.ModelForm):
    use_required_attribute = False
    class Meta:
        model = Cheques
        fields = ['cheque_type', 'cheque_for', 'cheque_number', 'bank_branch', 'cheque_amount',
                    'registered', 'cheque_image', 'export_receive_date', 'due_date', 'account_owner',
                    'project', 'account_party']
    
    def __init__(self, *args, **kwargs):
        url_name = kwargs.pop('url_name')
        super(ChequesForm, self).__init__(*args, **kwargs)

        self.fields['cheque_for'] = forms.CharField(
            label="بابت",
            validators=[none_numeric_value]
        )

        self.fields['bank_branch'] = forms.CharField(
            label="بانک و شعبه",
            validators=[none_numeric_value]
        )

        self.fields['account_owner'] = forms.CharField(
            label="صاحب حساب",
            validators=[none_numeric_value]
        )

        self.fields['account_party'] = forms.CharField(
            label="طرف حساب",
            validators=[none_numeric_value]
        )

        self.fields['cheque_amount'] = forms.IntegerField(
            label="مبلغ",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار مبلغ چک نمی‌تواند صفر باشد"
                )
            ]
        )

        if url_name == 'cheque_create':
            self.fields['export_receive_date'] = forms.DateTimeField(
                label="تاریخ صدور / دریافت",
                widget=forms.DateTimeInput(
                    attrs={
                        'value': ""
                    }
                )
            )

            self.fields['due_date'] = forms.DateTimeField(
                label="تاریخ سررسید",
                widget=forms.DateTimeInput(
                    attrs={
                        'value': ""
                    }
                )
            )