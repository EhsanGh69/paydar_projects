from django import forms
from django.core import validators

from utils.tools import none_numeric_value

from .models import Stuff, MainWarehouseImport




class StuffForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Stuff
        fields = ['stuff_type', 'measurement_unit']

    def __init__(self, *args, **kwargs):
        super(StuffForm, self).__init__(*args, **kwargs)

        self.fields['stuff_type'] = forms.CharField(
            label="نوع کالا",
            validators=[none_numeric_value]
        )



class MainWarehouseImportForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = MainWarehouseImport
        fields = ['supplier', 'other_sender', 'stuff_type', 'measurement_unit', 'stuff_amount',
                   'receiver', 'date_time', 'is_returned', 'project_returned',]
    
    def __init__(self, *args, **kwargs):
        url_name = kwargs.pop('url_name')
        super(MainWarehouseImportForm, self).__init__(*args, **kwargs)

        self.fields['stuff_amount'] = forms.IntegerField(
            label="مقدار",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار کالا نمی‌تواند صفر باشد"
                )
            ]
        )

        if url_name == 'warehouse_import_create':
            self.fields['date_time'] = forms.DateTimeField(
                label="تاریخ ارسال",
                widget=forms.DateTimeInput(
                    attrs={
                        'value': ""
                    }
                )
            )


