from django import forms
from django.core import validators



from .models import Owners, Project
from utils.tools import none_numeric_value



class OwnerForm(forms.ModelForm):
    use_required_attribute = False
    class Meta:
        model = Owners
        fields = ['full_name', 'phone', 'national_card_image', 'birth_certificate_image', 'ownership_document_image']

    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)

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


class ProjectForm(forms.ModelForm):
    use_required_attribute = False
    class Meta:
        model = Project
        fields = ['title', 'contract_type', 'owners', 'contractual_salary', 'contractual_percentage']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['title'] = forms.CharField(
            label="عنوان پروژه",
            validators=[none_numeric_value]
        )

        self.fields['owners'].help_text = """برای انتخاب بیش از یک مورد:
                                             <br>
                                             در ویندوز دکمه 'Ctrl' را نگه دارید
                                             <br>
                                             در اندروید انگشت خود را برروی گزینه مورد نظر نگه دارید
                                          """

        









