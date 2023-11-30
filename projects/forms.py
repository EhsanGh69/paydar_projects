from django import forms
from django.core import validators

from .models import Owners, Project, WorkReference, Costs, PaymentsImages
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

        self.fields['owners'].help_text = """برای انتخاب یا حذف بیش از یک مورد:
                                             <br>
                                             در ویندوز دکمه 'Ctrl' را نگه دارید
                                             <br>
                                             در اندروید انگشت خود را برروی گزینه مورد نظر نگه دارید
                                          """


class WorkReferenceForm(forms.ModelForm):
    use_required_attribute = False
    class Meta:
        model = WorkReference
        fields = ['project', 'activity_type', 'referrer', 'doing_agent', 'follow_confirm', 'follow_date', 'result_explan']

    def __init__(self, *args, **kwargs):
        super(WorkReferenceForm, self).__init__(*args, **kwargs)

        self.fields['activity_type'] = forms.CharField(
            label="نوع فعالیت",
            validators=[none_numeric_value]
        )

        self.fields['referrer'] = forms.CharField(
            label="ارجاع دهنده",
            validators=[none_numeric_value]
        )

        self.fields['doing_agent'] = forms.CharField(
            label="مأمور انجام",
            validators=[none_numeric_value]
        )


class CostsForm(forms.ModelForm):
    use_required_attribute = False
    class Meta:
        model = Costs
        fields = ['project', 'water_branch', 'electricity_branch', 'gas_branch', 'phone_subscription', 
                  'designer_office', 'supervisors', 'engineer_system', 'sketch_map', 'export_permit', 'export_end_work']
        
    def __init__(self, *args, **kwargs):
        super(CostsForm, self).__init__(*args, **kwargs)

        self.fields['water_branch'] = forms.IntegerField(
            label="هزینه انشعاب آب",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار هزینه انشعاب آب نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['electricity_branch'] = forms.IntegerField(
            label="هزینه انشعاب برق",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار هزینه انشعاب برق نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['gas_branch'] = forms.IntegerField(
            label="هزینه انشعاب گاز",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار هزینه انشعاب گاز نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['phone_subscription'] = forms.IntegerField(
            label="هزینه اشتراک تلفن",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار هزینه اشتراک تلفن نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['designer_office'] = forms.IntegerField(
            label="هزینه دفتر طراح",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار هزینه دفتر طراح نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['supervisors'] = forms.IntegerField(
            label="هزینه ناظرین",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار هزینه ناظرین نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['engineer_system'] = forms.IntegerField(
            label="هزینه نظام مهندسی",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار هزینه نظام مهندسی نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['sketch_map'] = forms.IntegerField(
            label="هزینه نقشه کروکی",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار هزینه نقشه کروکی نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['export_permit'] = forms.IntegerField(
            label="هزینه صدور پروانه",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار هزینه صدور پروانه نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['export_end_work'] = forms.IntegerField(
            label="هزینه صدور پایان کار",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار هزینه صدور پایان کار نمی‌تواند صفر باشد"
                )
            ]
        )


class PaymentsImagesForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = PaymentsImages
        fields = ['project', 'designer_office', 'supervisors', 'engineer_system',
                  'sketch_map', 'export_permit', 'visit_toll', 'education_share',
                  'fire_stations_share', 'social_security_share']

