from django import forms
from django.core import validators

from utils.tools import none_numeric_value

from .models import Contracts, Proceedings, Agreements, BankReceipts, ConditionStatements, RegisteredDocs, OfficialDocs






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


class ProceedingsForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Proceedings
        fields = ['project', 'account_party', 'proceeding_type', 'proceeding_image', 'proceeding_date']

    def __init__(self, *args, **kwargs):
        super(ProceedingsForm, self).__init__(*args, **kwargs)

        self.fields['account_party'] = forms.CharField(
            label="طرف حساب",
            validators=[none_numeric_value]
        )



class AgreementsForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Agreements
        fields = ['project', 'account_party', 'agreement_image', 'agreement_date']

    def __init__(self, *args, **kwargs):
        super(AgreementsForm, self).__init__(*args, **kwargs)

        self.fields['account_party'] = forms.CharField(
            label="طرف حساب",
            validators=[none_numeric_value]
        )



class BankReceiptsForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = BankReceipts
        fields = ['project', 'receive_or_pay', 'receipt_date', 'receipt_image']



class ConditionStatementsForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = ConditionStatements
        fields = ['project', 'contractor', 'work_unit', 'requested_amount', 'confirmed_amount', 
                  'accounting_confirm', 'management_confirm', 'final_deposit_amount']
        
    def __init__(self, *args, **kwargs):
        super(ConditionStatementsForm, self).__init__(*args, **kwargs)
        


class RegisteredDocsForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = RegisteredDocs
        fields = ['project', 'doc_type', 'doc_image']



class OfficialDocsForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = OfficialDocs
        fields = ['project', 'doc_type', 'letter_type', 'license_type',
                   'doc_title', 'doc_image', 'send_receive_date']


