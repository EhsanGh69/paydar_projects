from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum

import jdatetime



def none_numeric_value(value):
    try:
        is_numeric = type(int(value)) is int
    except Exception:
        return True
    
    if is_numeric :
            raise ValidationError("مقدار این فیلد نمی‌تواند عددی می‌باشد", params={"value": value})
    


def fund_validation(**kwargs):
    full_name = kwargs['form'].cleaned_data.get('full_name')
    operation_type = kwargs['form'].cleaned_data.get('operation_type')
    if operation_type == 'rem':
        cost_amount = kwargs['form'].cleaned_data.get('cost_amount')
        cost_description = kwargs['form'].cleaned_data.get('cost_description')
        receipt_image = kwargs['form'].cleaned_data.get('receipt_image')
        fund_person = kwargs['model'].objects.filter(full_name=full_name)
        if fund_person:
            if cost_amount == 0:
                kwargs['form'].add_error('cost_amount', 'لطفا مبلغ هزینه را وارد نمایید')
                return False
            elif cost_description == '':
                kwargs['form'].add_error('cost_description', 'لطفا شرح هزینه را وارد نمایید')
                return False
            elif kwargs['url_name'] == 'fund_create' and receipt_image is None:
                kwargs['form'].add_error('receipt_image', 'لطفا تصویر فیش پرداختی را بارگذاری نمایید')
                return False
            else:
                sum_costs = fund_person.aggregate(Sum('cost_amount'))['cost_amount__sum']
                sum_charge = fund_person.aggregate(Sum('charge_amount'))['charge_amount__sum']
                total_cash = (sum_charge - sum_costs) - cost_amount
                if total_cash <= 0:
                    kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["موجودی تنخواه جهت برداشت کافی نمی‌باشد."])
                    return False
                else:
                    return True
        else:
            kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["تنخواه جدید هیچ موجودی جهت برداشت ندارد."])
            return False
    else:
        charge_amount = kwargs['form'].cleaned_data.get('charge_amount')
        charge_date = kwargs['form'].cleaned_data.get('charge_date')
        charge_image = kwargs['form'].cleaned_data.get('charge_image')
        if charge_amount == 0:
            kwargs['form'].add_error('charge_amount', 'لطفا مبلغ واریزی را وارد نمایید')
            return False
        elif charge_date is None:
            kwargs['form'].add_error('charge_date', 'لطفا تاریخ واریز را وارد نمایید')
            return False
        elif kwargs['url_name'] == 'fund_create' and charge_image is None:
            kwargs['form'].add_error('charge_image', 'لطفا تصویر فیش واریزی را بارگذاری نمایید')
            return False
        else:
            return True


def cash_box_validation(**kwargs):
    operation_type = kwargs['form'].cleaned_data.get('operation_type')

    if operation_type == 'rem':
        removal_amount = kwargs['form'].cleaned_data.get('removal_amount')
        removal_description = kwargs['form'].cleaned_data.get('removal_description')
        removal_image = kwargs['form'].cleaned_data.get('removal_image')
        rem_operate = kwargs['model'].objects.filter(operation_type='rem')
        set_operate = kwargs['model'].objects.filter(operation_type='set')

        if set_operate:

            if removal_amount == 0:
                kwargs['form'].add_error('removal_amount', 'لطفا مبلغ برداشت را وارد نمایید')
                return False
            elif removal_description == '':
                kwargs['form'].add_error('removal_description', 'لطفا شرح برداشت را وارد نمایید')
                return False
            elif kwargs['url_name'] == 'cash_box_create' and removal_image is None:
                kwargs['form'].add_error('removal_image', 'لطفا تصویر فیش برداشت را بارگذاری نمایید')
                return False
            elif not rem_operate:
                sum_settles = set_operate.aggregate(Sum('settle_amount'))['settle_amount__sum']
                total_cash = sum_settles - removal_amount
                if total_cash <= 0:
                    kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["موجودی صندوق جهت برداشت کافی نمی‌باشد."])
                    return False
                else:
                    return True
            else:
                sum_removals = rem_operate.aggregate(Sum('removal_amount'))['removal_amount__sum']
                sum_settles = set_operate.aggregate(Sum('settle_amount'))['settle_amount__sum']
                total_cash = (sum_settles - sum_removals) - removal_amount
                if total_cash <= 0:
                    kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["موجودی صندوق جهت برداشت کافی نمی‌باشد."])
                    return False
                else:
                    return True
        else:
            kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["صندوق هیچ موجودی جهت برداشت ندارد."])
            return False
    
    else:
        settle_amount = kwargs['form'].cleaned_data.get('settle_amount')
        settle_description = kwargs['form'].cleaned_data.get('settle_description')
        settle_image = kwargs['form'].cleaned_data.get('settle_image')

        if settle_amount == 0:
            kwargs['form'].add_error('settle_amount', 'لطفا مبلغ واریزی را وارد نمایید')
            return False
        elif settle_description == '':
            kwargs['form'].add_error('settle_description', 'لطفا شرح واریز را وارد نمایید')
            return False
        elif kwargs['url_name'] == 'cash_box_create' and settle_image is None:
            kwargs['form'].add_error('settle_image', 'لطفا تصویر فیش برداشت را بارگذاری نمایید')
            return False
        else:
            return True


def warehouse_export_validation(**kwargs):
    imp_stuff_amount = kwargs['imp_model'].objects.filter(stuff_type=kwargs['stuff_type']).aggregate(Sum('stuff_amount'))['stuff_amount__sum']
    exp_stuff_amount = kwargs['exp_model'].objects.filter(stuff_type=kwargs['stuff_type']).aggregate(Sum('stuff_amount'))['stuff_amount__sum']
    total_stuff_amount = 0

    if imp_stuff_amount:
    
        if not exp_stuff_amount:
            total_stuff_amount = imp_stuff_amount
        else:
            total_stuff_amount = imp_stuff_amount - exp_stuff_amount

        if  kwargs['stuff_amount'] > total_stuff_amount:
            kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["موجودی کالا در انبار کافی نمی‌باشد."])
            return False
        else:
            return True
        
    else:
        kwargs['form'].errors['__all__'] = kwargs['form'].error_class(["کالا در انبار هیچ موجودی ندارد."])
        return False



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
    

     