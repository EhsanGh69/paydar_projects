from django import forms
from django.core import validators

from utils.tools import none_numeric_value

from .models import Stuff, MainWarehouseImport




class StuffForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Stuff
        fields = ['stuff_type', 'measurement_unit']

    def __init__(self,  *args, **kwargs):
        super(StuffForm, self).__init__( *args, **kwargs)

        self.fields['stuff_type'] = forms.CharField(
            label="نوع کالا",
            validators=[none_numeric_value]
        )




