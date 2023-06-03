from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


from .models import Receive


def none_numeric_value(value):
    try:
        is_numeric = type(int(value)) is int
    except Exception:
        return True

    if is_numeric:
        raise ValidationError("مقدار این فیلد نمی‌تواند عددی می‌باشد", params={"value": value})


class ReceiveForm(forms.ModelForm):
    use_required_attribute = False

    def __int__(self, *args, **kwargs):
        super(ReceiveForm, self).__int__(*args, **kwargs)

        self.fields['receive_amount'] = forms.IntegerField(
            label="مبلغ دریافتی",
            validators=[
                validators.MinValueValidator(
                    limit_value=1,
                    message="مقدار مبلغ دریافتی نمی‌تواند صفر باشد"
                )
            ]
        )

        self.fields['receive_for'] = forms.CharField(
            label="دریافت بابت",
            validators=[none_numeric_value]
        )

    class Meta:
        model = Receive
        fields = ['organization', 'receive_for', 'project', 'receive_amount', 'receive_date']

    
