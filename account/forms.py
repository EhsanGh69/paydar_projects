from django import forms
from django.core import validators
from django.contrib.auth.models import Group

from utils.tools import none_numeric_value, valid_select_permissions, password_validation

from .models import User



class UserLogin(forms.Form):
    use_required_attribute = False

    username = forms.CharField(
        widget=forms.TextInput(),
        required=False,
        label='نام کاربری'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label='رمز عبور'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('لطفاً نام کاربری خود را وارد نمایید')
        
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('لطفاً رمز عبور خود را وارد نمایید')
        
        return password


class UserChangePassword(forms.Form):
    use_required_attribute = False

    old_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label='رمز عبور کنونی'
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label='رمز عبور جدید'
    )

    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label='تأیید رمز عبور جدید'
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not old_password:
            raise forms.ValidationError('لطفاً رمز عبور کنونی خود را وارد نمایید')
        
        return old_password
    
    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if not new_password:
            raise forms.ValidationError('لطفاً رمز عبور جدید خود را وارد نمایید')
        
        return new_password
    
    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if not confirm_new_password and new_password:
            raise forms.ValidationError('لطفاً رمز عبور جدید خود تأیید نمایید')
        if new_password and confirm_new_password != new_password:
            raise forms.ValidationError('تأیید رمز عبور جدید با رمز عبور جدید یکسان نیست')
        
        return confirm_new_password


class UserEditAccount(forms.Form):
    use_required_attribute = False

    mobile_number = forms.CharField(
        widget=forms.TextInput(),
        required=False,
        label='شماره همراه',
        validators=[
            validators.RegexValidator(
                regex=r'^09\d{9}$',
                message='شماره همراه وارد شده معتبر نمی‌باشد'
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

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number:
            raise forms.ValidationError('لطفاً شماره همراه خود را وارد نمایید')
        
        return mobile_number

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('لطفاً نام خود را وارد نمایید')
        
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError('لطفاً نام خانوادگی خود را وارد نمایید')
        
        return last_name


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
        required=False,
        label='گروه‌های دسترسی' 
    )

    mobile_number = forms.CharField(
        widget=forms.TextInput(),
        required=True,
        label='شماره همراه',
        validators=[
            validators.RegexValidator(
                # regex=r'^09\d{9}$',
                regex=r'^(?:(?:(?:\\+?|00)(98))|(0))?((?:90|91|92|93|99)[0-9]{8})$',
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
        
        for char in username: # type: ignore
            err_count = 0
            for valid_range in valid_ranges:
                if ord(char) not in valid_range:
                    err_count += 1
            if err_count == 4:
                raise forms.ValidationError('نام کاربری وارد شده دارای کاراکتر یا کاراکترهای غیرمجاز می‌باشد')
                
        return username


    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        check_password = password_validation(password, username) # type: ignore
        
        if check_password == "similar_err":
            raise forms.ValidationError('رمز عبور نباید شبیه نام کاربری باشد')
        elif check_password == "combine_err":
            raise forms.ValidationError('رمز عبور باید ترکیبی از حروف و اعداد باشد')
        
        return password


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('تأیید رمز عبور با رمز عبور وارد شده یکسان نیست')
        
        return confirm_password
    

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        is_exits_mobile_number = User.objects.filter(mobile_number=mobile_number).exists()

        if is_exits_mobile_number:
            raise forms.ValidationError('شماره همراه وارد شده از قبل وجود دارد، لطفا شماره همراه دیگری وارد کنید')
        
        return mobile_number


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
                regex=r'^(?:(?:(?:\\+?|00)(98))|(0))?((?:90|91|92|93|99)[0-9]{8})$',
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
        for char in username: # type: ignore
            err_count = 0
            for valid_range in valid_ranges:
                if ord(char) not in valid_range:
                    err_count += 1
            if err_count == 4:
                raise forms.ValidationError('نام کاربری وارد شده دارای کاراکتر یا کاراکترهای غیرمجاز می‌باشد')
        
        return username
        

class AddGroupForm(forms.Form):
    use_required_attribute = False
    PERMISSIONS_CHOICES = valid_select_permissions
    
    group_name = forms.CharField(
        widget=forms.TextInput(),
        required=True,
        label='نام گروه'
    )

    permissions = forms.MultipleChoiceField(
        choices=PERMISSIONS_CHOICES,
        required=True,
        label='‌دسترسی‌ها'
    )

    def clean_group_name(self):
        group_name = self.cleaned_data.get('group_name')
        is_exits_group_name = Group.objects.filter(name=group_name).exists()
        if is_exits_group_name:
            raise forms.ValidationError('گروه دسترسی با این نام وجود دارد، لطفا نام دیگری وارد کنید')
        
        return group_name
        

class UpdateGroupForm(forms.Form):
    use_required_attribute = False
    PERMISSIONS_CHOICES = valid_select_permissions
    
    group_name = forms.CharField(
        widget=forms.TextInput(),
        required=True,
        label='نام گروه'
    )

    permissions = forms.MultipleChoiceField(
        choices=PERMISSIONS_CHOICES,
        required=True,
        label='‌دسترسی‌ها'
    )
