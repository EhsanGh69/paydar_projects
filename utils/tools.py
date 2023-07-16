from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

import jdatetime



def none_numeric_value(value):
    try:
        is_numeric = type(int(value)) is int
    except Exception:
        return True
    
    if is_numeric :
            raise ValidationError("مقدار این فیلد نمی‌تواند عددی می‌باشد", params={"value": value})
    


def fund_rem_validation(**kwargs):
    fund_person = kwargs['model'].objects.filter(full_name=kwargs['name'])
    
    if fund_person:
                
        if kwargs['cost'] == 0 or kwargs['cost'] is None:
            kwargs['form'].add_error('cost_amount', 'لطفا مبلغ هزینه را وارد نمایید')
        elif kwargs['desc'] == '' or kwargs['desc'] is None:
            kwargs['form'].add_error('cost_description', 'لطفا شرح هزینه را وارد نمایید')

        else:
            sum_costs = fund_person.aggregate(Sum('cost_amount'))
            sum_charge = fund_person.aggregate(Sum('charge_amount'))
            check_cash = (sum_charge['charge_amount__sum'] - sum_costs['cost_amount__sum']) - kwargs['cost']
            if check_cash <= 0:
                kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["موجودی تنخواه جهت برداشت کافی نمی‌باشد."])
            try:
                receipt_image = kwargs['req'].FILES['receipt_image']
                fs = FileSystemStorage()
                file_name = fs.save(receipt_image.name, receipt_image)
                
                if kwargs['obj_id']:
                    kwargs['model'].objects.filter(pk=kwargs['obj_id']).update(full_name=kwargs['name'], operation_type='rem', 
                                                                        cost_amount=kwargs['cost'], cost_description=kwargs['desc'], receipt_image=file_name)
                    messages.success(kwargs['req'], "عملیات تنخواه با موفقیت ویرایش شد")
                    return True
                else:
                    kwargs['model'].objects.create(full_name=kwargs['name'], operation_type='rem',
                                        cost_amount=kwargs['cost'], cost_description=kwargs['desc'], receipt_image=file_name)
                    messages.success(kwargs['req'], "عملیات تنخواه با موفقیت انجام شد")
                    return True
            except Exception:
                if kwargs['obj_id']:
                    kwargs['model'].objects.filter(pk=kwargs['obj_id']).update(full_name=kwargs['name'], operation_type='rem', 
                                                                        cost_amount=kwargs['cost'], cost_description=kwargs['desc'])
                    messages.success(kwargs['req'], "عملیات تنخواه با موفقیت ویرایش شد")
                    return True
                else:
                    kwargs['form'].add_error('receipt_image', 'لطفا تصویر فیش پرداختی را بارگذاری نمایید')

    else:
        kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["تنخواه جدید هیچ موجودی جهت برداشت ندارد."])


def fund_set_validation(**kwargs):
    if kwargs['charge'] == 0 or kwargs['charge'] is None:
        kwargs['form'].add_error('charge_amount', 'لطفا مبلغ شارژ را وارد نمایید')
    elif kwargs['date'] == '' or kwargs['date'] is None:
        kwargs['form'].add_error('charge_date', 'لطفا تاریخ واریز را وارد نمایید')

    else:
        try:
            charge_image = kwargs['req'].FILES['charge_image']
            fs = FileSystemStorage()
            file_name = fs.save(charge_image.name, charge_image)
    
            if kwargs['obj_id']:
                kwargs['model'].objects.filter(pk=kwargs['obj_id']).update(full_name=kwargs['name'], operation_type='set',
                                                                    charge_amount=kwargs['charge'], charge_date=kwargs['date'], charge_image=file_name)
                
                messages.success(kwargs['req'], "عملیات تنخواه با موفقیت ویرایش شد")
                return True
            else:
                kwargs['model'].objects.create(full_name=kwargs['name'], operation_type='set',
                                    charge_amount=kwargs['charge'], charge_date=kwargs['date'], charge_image=file_name)
                messages.success(kwargs['req'], "عملیات تنخواه با موفقیت انجام شد")
                return True
        except Exception:
            if kwargs['obj_id']:
                kwargs['model'].objects.filter(pk=kwargs['obj_id']).update(full_name=kwargs['name'], operation_type='set',
                                                                    charge_amount=kwargs['charge'], charge_date=kwargs['date'])
                messages.success(kwargs['req'], "عملیات تنخواه با موفقیت ویرایش شد")
                return True
            else:
                kwargs['form'].add_error('charge_image', 'لطفا تصویر فیش واریزی را بارگذاری نمایید')



def filter_date_values(filter_value):
    now_day = timezone.now().day
    now_month = timezone.now().month
    now_year = timezone.now().year

    now_date_str = f'{now_year}-{now_month}-{now_day}'

    last_week = now_day - 7
    last_month = now_month - 1
    last_year = now_year - 1
    
    if filter_value == "last_week":
        if last_week > 0:
            return [f'{now_year}-{now_month}-{last_week}', now_date_str]
        elif last_month > 0:
            return [f'{now_year}-{last_month}-{last_week + 31}', now_date_str]
        else:
            return [f'{last_year}-{12}-{last_week + 31}', now_date_str]
    elif filter_value == "last_month":
        if last_month > 0:
            return [f'{now_year}-{last_month}-{now_day}', now_date_str]
        else:
            return [f'{last_year}-{12}-{now_day}', now_date_str]
    elif filter_value == "current_year":
        greg_tuple = jdatetime.JalaliToGregorian(jdatetime.datetime.now().year, 1, 1).getGregorianList()
        return [f'{greg_tuple[0]}-{greg_tuple[1]}-{greg_tuple[2]}', now_date_str]
    else:
        return [now_date_str, now_date_str]
    

     