from government_accounts.models import Receive, Payment, Activity
from non_government_accounts.models import BuyersSellers, Orders
from projects.models import WorkReference
from cheques_receive_pay.models import Cheques, ReceivePay, Fund
from warehousing.models import MainWarehouseImport
from projects_docs.models import BankReceipts
from account.models import Report

from  jdatetime import JalaliToGregorian



def jdate_to_str_gdate(jdate):
    splitted_date = str(jdate).split("-")
    greg_date_tuple = JalaliToGregorian(int(splitted_date[0]), int(splitted_date[1]), int(splitted_date[2])).getGregorianList()
    formatted_greg_date = "{}-{}-{}".format(greg_date_tuple[0], greg_date_tuple[1], greg_date_tuple[2])
    return formatted_greg_date



def date_query(start_date:str, end_date:str, validation:bool=False, search:bool=False, model_name:str=""):
    formatted_greg_start_date = jdate_to_str_gdate(start_date)
    formatted_greg_end_date = jdate_to_str_gdate(end_date)
    date_range = [formatted_greg_start_date, formatted_greg_end_date]

    start_date_query = Report.objects.filter(date_from=formatted_greg_start_date)
    end_date_query = Report.objects.filter(date_to=formatted_greg_end_date)

    if validation:
        if start_date_query.exists() and end_date_query.exists():
            return False
        else:
            return True
    elif search:
        return Report.objects.filter(date_from=formatted_greg_start_date, date_to=formatted_greg_end_date).all()
    else:
        global query_result
        if model_name == "receives":
            query_result = Receive.objects.filter(receive_date__date__range=date_range).all()
        elif model_name == "payments":
            query_result = Payment.objects.filter(payment_date__date__range=date_range).all()
        elif model_name == "activities":
            query_result = Activity.objects.filter(activity_date__date__range=date_range).all()
        elif model_name == "buyers_sellers":
            query_result = BuyersSellers.objects.filter(payment_date__date__range=date_range).all()
        elif model_name == "orders":
            query_result = Orders.objects.filter(order_date__date__range=date_range).all()
        elif model_name == "work_reference":
            query_result = WorkReference.objects.filter(follow_date__date__range=date_range).all()
        elif model_name == "cheques":
            query_result = Cheques.objects.filter(due_date__date__range=date_range).all()
        elif model_name == "fund":
            query_result = Fund.objects.filter(charge_date__date__range=date_range).all()
        elif model_name == "receive_pay":
            query_result = ReceivePay.objects.filter(date__date__range=date_range).all()
        elif model_name == "warehouse_import":
            query_result = MainWarehouseImport.objects.filter(date_time__date__range=date_range).all()
        elif model_name == "bank_receives":
            query_result = BankReceipts.objects.filter(receipt_date__range=date_range).all()
        else:
            return
        return query_result