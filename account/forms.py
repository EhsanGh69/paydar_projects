from django import forms
from django.core import validators
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm

from utils.tools import none_numeric_value

from .models import User



class AuthenticateForm(AuthenticationForm):
    use_required_attribute = False



class AddUserForm(forms.Form):
    use_required_attribute = False
    GROUP_CHOICES = [(group.name, group.name) for group in Group.objects.all()]

    username = forms.CharField(
        widget=forms.TextInput(),
        label='نام کاربری',
        required=True,
        validators=[
            validators.MaxLengthValidator(
                limit_value=20,
                message='تعداد کاراکترهای وارد شده بیشتر از حد مجاز است'
            ),
            validators.MinLengthValidator(
                limit_value=4,
                message='تعداد کاراکترهای وارد شده کمتر از حد مجاز است'
            ),
        ],
        help_text='''تعداد کاراکترهای مجاز حداقل ۴ و حداکثر ۲۰ می‌باشد
                    <br>
                    فقط شامل حروف، اعداد، و علامات @/./+/-/_
                  '''
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label='رمز عبور',
        validators=[
            validators.MinLengthValidator(
                limit_value=8,
                message='تعداد کاراکترهای وارد شده کمتر از حد مجاز است'
            )
        ],
        help_text='''رمز عبور نباید شبیه نام کاربری باشد
                     <br>
                     رمز عبور شما می‌بایست حداقل از ۸ کاراکتر شامل حروف و اعداد تشکیل شده باشد
                  '''
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label='تأیید رمز عبور',
    )

    access_groups = forms.MultipleChoiceField(
        choices=GROUP_CHOICES,
        required=True,
        label='گروه‌های دسترسی'              
    )

    mobile_number = forms.CharField(
        widget=forms.TextInput(),
        required=True,
        label='شماره همراه',
        validators=[
            validators.RegexValidator(
                regex=r'^0\d{10}$',
                message="شماره همراه وارد شده معتبر نمی‌باشد"
            )
        ]
    )

    first_name = forms.CharField(
        widget=forms.TextInput(),
        validators=[none_numeric_value],
        required=False,
        label='نام'
    )

    last_name = forms.CharField(
        widget=forms.TextInput(),
        validators=[none_numeric_value],
        required=False,
        label='نام خانوادگی'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exits_username = User.objects.filter(username=username).exists()
        valid_ranges = [range(48, 58), range(65, 91), range(97, 123), [43, 45, 46, 64, 95]]
       
        if is_exits_username:
            raise forms.ValidationError('کاربری با نام کاربری وارد شده وجود دارد، لطفا نام کاربری دیگری وارد کنید')
        
        for char in username:
            err_count = 0
            for valid_range in valid_ranges:
                if ord(char) not in valid_range:
                    err_count += 1
            if err_count == 4:
                raise forms.ValidationError('نام کاربری وارد شده دارای کاراکتر یا کاراکترهای غیرمجاز می‌باشد')
                
        return username


    def clean_password(self):
        password = self.cleaned_data.get('password')
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        
        list_control = []
        for char in password:
            if char in nums:
                list_control.append('n')
            else:
                list_control.append('l')
        if 'n' not in list_control or 'l' not in list_control:
            raise forms.ValidationError('رمز عبور باید ترکیبی از حروف و اعداد باشد')
        
        return password


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('تأیید رمز عبور با رمز عبور وارد شده یکسان نیست')
        
        return confirm_password



class UpdateUserForm(forms.Form):
    use_required_attribute = False
    GROUP_CHOICES = [(group.name, group.name) for group in Group.objects.all()]

    username = forms.CharField(
        widget=forms.TextInput(),
        label='نام کاربری',
        required=True,
        validators=[
            validators.MaxLengthValidator(
                limit_value=20,
                message='تعداد کاراکترهای وارد شده بیشتر از حد مجاز است'
            ),
            validators.MinLengthValidator(
                limit_value=4,
                message='تعداد کاراکترهای وارد شده کمتر از حد مجاز است'
            ),
        ],
        help_text='''تعداد کاراکترهای مجاز حداقل ۴ و حداکثر ۲۰ می‌باشد
                    <br>
                    فقط شامل حروف، اعداد، و علامات @/./+/-/_
                  '''
    )

    access_groups = forms.MultipleChoiceField(
        choices=GROUP_CHOICES,
        required=True,
        label='گروه‌های دسترسی'              
    )

    mobile_number = forms.CharField(
        widget=forms.TextInput(),
        required=True,
        label='شماره همراه',
        validators=[
            validators.RegexValidator(
                regex=r'^0\d{10}$',
                message="شماره همراه وارد شده معتبر نمی‌باشد"
            )
        ]
    )

    first_name = forms.CharField(
        widget=forms.TextInput(),
        validators=[none_numeric_value],
        required=False,
        label='نام'
    )

    last_name = forms.CharField(
        widget=forms.TextInput(),
        validators=[none_numeric_value],
        required=False,
        label='نام خانوادگی'
    )

    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
        label='کاربر فعال',
        help_text="نشان می‌دهد که آیا این کاربر اجازهٔ فعالیت دارد یا خیر. به جای حذف کاربر این تیک را بردارید"
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        valid_ranges = [range(48, 58), range(65, 91), range(97, 123), [43, 45, 46, 64, 95]]
        for char in username:
            err_count = 0
            for valid_range in valid_ranges:
                if ord(char) not in valid_range:
                    err_count += 1
            if err_count == 4:
                raise forms.ValidationError('نام کاربری وارد شده دارای کاراکتر یا کاراکترهای غیرمجاز می‌باشد')
        
        return username
        
