from django import forms
from django.core import validators

from utils.tools import none_numeric_value

from .models import Stuff, MainWarehouseImport, MainWarehouseExport, UseCertificate, ProjectWarehouse




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


class MainWarehouseExportForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = MainWarehouseExport
        fields = ['personnel', 'contractor', 'stuff_type', 'measurement_unit', 
                  'stuff_amount', 'deliverer', 'project']
        
    def __init__(self, *args, **kwargs):
        super(MainWarehouseExportForm, self).__init__(*args, **kwargs)

        self.fields['stuff_amount'] = forms.IntegerField(
            label="مقدار",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار کالا نمی‌تواند صفر باشد"
                )
            ]
        )


class UseCertificateForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = UseCertificate
        fields = ['stuff_type', 'measurement_unit', 'is_deficient', 'deficient_amount', 'is_excess',
                  'excess_amount', 'start_using_date', 'finish_using_date', 'returned_to', 'return_date']
        

class ProjectWarehouseForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = ProjectWarehouse
        fields = ['project', 'personnel_apply', 'contractor_apply', 'stuff_type', 'measurement_unit', 
                  'stuff_amount', 'personnel_delivery', 'contractor_delivery', 'use_certificate', 'status']
        
    def __init__(self, *args, **kwargs):
        super(ProjectWarehouseForm, self).__init__(*args, **kwargs)
        
        self.fields['stuff_amount'] = forms.IntegerField(
                label="مقدار",
                validators=[
                    validators.MinValueValidator(
                        limit_value=1,
                        message="مقدار کالا نمی‌تواند صفر باشد"
                    )
                ]
            )

