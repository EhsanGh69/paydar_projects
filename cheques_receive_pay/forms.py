from django import forms
from django.core import validators


from .models import Cheques, Fund, ReceivePay, CashBox
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


class FundForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Fund
        fields = ['full_name', 'operation_type', 'cost_amount', 'cost_description', 'receipt_image',
                    'charge_amount', 'charge_date', 'charge_image']
    
    def __init__(self, *args, **kwargs):
        url_name = kwargs.pop('url_name')
        super(FundForm, self).__init__(*args, **kwargs)

        self.fields['full_name'] = forms.CharField(
            label="نام تنخواه",
            validators=[none_numeric_value]
        )

        if url_name == 'fund_create':
            self.fields['charge_date'] = forms.DateTimeField(
                label="تاریخ واریز",
                widget=forms.DateTimeInput(
                    attrs={
                        'value': ""
                    }
                )
            )

        self.fields['charge_date'].required = False
        self.fields['cost_amount'].help_text = 'جهت عملیات برداشت از تنخواه این فیلد لازم است'
        self.fields['receipt_image'].help_text = 'جهت عملیات برداشت از تنخواه این فیلد لازم است'
        self.fields['charge_amount'].help_text = 'جهت عملیات واریز به تنخواه این فیلد لازم است'
        self.fields['charge_image'].help_text = 'جهت عملیات واریز به تنخواه این فیلد لازم است'
    

class ReceivePayForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = ReceivePay
        fields = ['organ', 'contractor', 'supplier', 'personnel', 'receive_pay',
                   'amount', 'regard_to', 'date', 'receipt_image']
    
    def __init__(self, *args, **kwargs):
        url_name = kwargs.pop('url_name')
        super(ReceivePayForm, self).__init__(*args, **kwargs)


        self.fields['amount'] = forms.IntegerField(
            label="مبلغ",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار مبلغ نمی‌تواند صفر باشد"
                )
            ]
        )
        
        self.fields['regard_to'] = forms.CharField(
            label="بابت",
            validators=[none_numeric_value]
        )

        if url_name == 'receive_pay_create':
            self.fields['date'] = forms.DateTimeField(
                label="تاریخ",
                widget=forms.DateTimeInput(
                    attrs={
                        'value': ""
                    }
                )
            )



class CashBoxForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = CashBox
        fields = ['operation_type', 'settle_amount', 'settle_image', 'settle_description', 
                  'removal_amount', 'removal_image', 'removal_description']
        
    def __init__(self, *args, **kwargs):
        super(CashBoxForm, self).__init__(*args, **kwargs)

        self.fields['settle_amount'].help_text = 'جهت عملیات واریز به صندوق این فیلد لازم است'
        self.fields['settle_image'].help_text = 'جهت عملیات واریز به صندوق این فیلد لازم است'
        self.fields['removal_amount'].help_text = 'جهت عملیات برداشت از صندوق این فیلد لازم است'
        self.fields['removal_image'].help_text = 'جهت عملیات برداشت از صندوق این فیلد لازم است'