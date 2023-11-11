from django import forms
from django.core import validators


from .models import Contractors, Suppliers, Personnel, Partners, BuyersSellers, Orders, ConflictOrders

from utils.tools import none_numeric_value



class ContractorForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Contractors
        fields = ['project', 'full_name', 'job', 'phone', 'address']

    def __init__(self, *args, **kwargs):
        super(ContractorForm, self).__init__(*args, **kwargs)

        self.fields['full_name'] = forms.CharField(
            label="نام و نام خانوادگی",
            validators=[none_numeric_value]
        )

        self.fields['job'] = forms.CharField(
            label="رشته شغلی",
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


class SupplierForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Suppliers
        fields = ['project', 'full_name', 'job', 'phone', 'address']

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)

        self.fields['full_name'] = forms.CharField(
            label="نام و نام خانوادگی",
            validators=[none_numeric_value]
        )

        self.fields['job'] = forms.CharField(
            label="رشته شغلی",
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


class PersonnelForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Personnel
        fields = ['full_name', 'job', 'phone', 'address', 'contract_image']

    def __init__(self, *args, **kwargs):
        super(PersonnelForm, self).__init__(*args, **kwargs)

        self.fields['full_name'] = forms.CharField(
            label="نام و نام خانوادگی",
            validators=[none_numeric_value]
        )

        self.fields['job'] = forms.CharField(
            label="رشته شغلی",
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


class PartnersForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Partners
        fields = ['investment_amount', 'project', 'contract_image', 'full_name', 'address', 'phone']

    def __init__(self, *args, **kwargs):
        super(PartnersForm, self).__init__(*args, **kwargs)

        self.fields['investment_amount'] = forms.IntegerField(
            label="مبلغ سرمایه‌گذاری",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار مبلغ سرمایه‌گذاری نمی‌تواند صفر باشد"
                )
            ]
        )

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


class BuyersSellersForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = BuyersSellers
        fields = ['project', 'buyer_seller', 'full_name', 'phone', 'address',
                  'contract_image', 'payment_order', 'current_roof', 'payment_date', 'payment_amount']

    def __init__(self, *args, **kwargs):
        url_name = kwargs.pop('url_name')
        super(BuyersSellersForm, self).__init__(*args, **kwargs)

        self.fields['payment_amount'] = forms.IntegerField(
            label="مبلغ پرداختی",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار مبلغ پرداختی نمی‌تواند صفر باشد"
                )
            ]
        )

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

        if url_name == 'buyer_seller_create':
            self.fields['payment_date'] = forms.DateTimeField(
                label="تاریخ و ساعت پرداخت",
                widget=forms.DateTimeInput(
                    attrs={
                        'value': ""
                    }
                )
            )
        

        self.fields['current_roof'] = forms.CharField(
            label="سقف کنونی",
            widget=forms.DateTimeInput(
                attrs={
                    'disabled': "disabled"
                }
            )
        )
        self.fields['current_roof'].required = False
        self.fields['current_roof'].help_text = "اگر ترتیب پرداخت از نوع 'بعد از سقف طبقه' باشد، این فیلد اجباری است"


class OrdersForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Orders
        fields = ['supplier', 'order_type', 'measurement_unit', 'unit_price', 'order_amount',
                  'order_date', 'order_respite', 'order_result', 'sending_date',
                  'sended_image', 'sended_image_type', 'explan_order_cancel', 'project']
        
    def __init__(self, *args, **kwargs):
        url_name = kwargs.pop('url_name')
        super(OrdersForm, self).__init__(*args, **kwargs)

    
        self.fields['order_type'] = forms.CharField(
            label="نوع سفارش",
            validators=[none_numeric_value]
        )

        self.fields['unit_price'] = forms.IntegerField(
            label="قیمت واحد",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار قیمت واحد نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['order_amount'] = forms.IntegerField(
            label="مقدار سفارش",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار سفارش نمی‌تواند صفر باشد"
                )
            ]
        )

        if url_name == 'order_create':
            self.fields['order_date'] = forms.DateTimeField(
                label="تاریخ و ساعت سفارش",
                widget=forms.DateTimeInput(
                    attrs={
                        "value": ""
                    }
                )
            )

            self.fields['sending_date'] = forms.DateTimeField(
                label="تاریخ و ساعت ارسال سفارش",
                widget=forms.DateTimeInput(
                    attrs={
                        "value": ""
                    }
                )
            )


        self.fields['order_respite'] = forms.IntegerField(
            label="مهلت سفارش",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مهلت سفارش نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['sending_date'].required = False
        self.fields['sending_date'].help_text = "اگر نتیجه سفارش 'ارسال در تاریخ مشخص' باشد، این فیلد اجباری است"

        self.fields['order_respite'].help_text = "بر اساس روز"

        self.fields['sended_image'].required = False
        self.fields['sended_image_type'].required = False


class ConflictOrdersForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = ConflictOrders
        fields = ['order', 'conflict_type', 'conflict_amount']

    def __init__(self, *args, **kwargs):
        super(ConflictOrdersForm, self).__init__(*args, **kwargs)

        self.fields['conflict_amount'] = forms.IntegerField(
            label="مقدار مغایرت",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار مغایرت نمی‌تواند صفر باشد"
                )
            ]
        )



