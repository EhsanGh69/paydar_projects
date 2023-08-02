from django import forms
from django.core import validators

from utils.tools import none_numeric_value

from .models import Contracts






class ContractsForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Contracts
        fields = ['related_to_project', 'unrelated_to_project', 'contract_type', 'contract_title', 'contract_party',
                  'contract_image', 'contract_date']
    
    def __init__(self, *args, **kwargs):
        super(ContractsForm, self).__init__(*args, **kwargs)

        self.fields['contract_title'] = forms.CharField(
            label="عنوان قرارداد",
            validators=[none_numeric_value]
        )

        self.fields['contract_party'] = forms.CharField(
            label="طرف قرارداد",
            validators=[none_numeric_value]
        )





