from django import template
from django.utils.html import format_html

register = template.Library()

@register.inclusion_tag("partials/main_menu.html")
def main_menu(request, app_name, list_path_name, create_path_name, update_path_name, search_path_name, icon_type, list_content):
    return {
        "request": request,
        "all_paths": [list_path_name, create_path_name, update_path_name, search_path_name],
        "list_link_name": "{}:{}".format(app_name, list_path_name),
        "icon_type": icon_type,
        "list_content": list_content,
    }

@register.filter()
def min(value, arg):
    return value - arg

@register.filter()
def to_int(value):
    return int(value)

@register.inclusion_tag("partials/objects_records.html")
def objects_records(list_url, search_url, record_number, records_count, fields_order, order_by, list_filters=None, have_order=True):
    return {
        "list_url": list_url,
        "search_url": search_url,
        "record_number": record_number,
        "records_count": records_count,
        "fields_order": fields_order,
        "order_by": order_by,
        "list_filters": list_filters,
        "have_order": have_order
    }

@register.inclusion_tag("partials/pagination_urls.html")
def pagination_urls(previous_url, item_url, next_url, record_number, list_url, search_url, list_filters, order_by, page_obj, page_item):
    return {
        "previous_url": previous_url,
        "item_url": item_url,
        "next_url": next_url,
        "list_url": list_url,
        "search_url": search_url,
        "record_number": record_number,
        "list_filters": list_filters,
        "order_by": order_by,
        "page_obj": page_obj,
        "page_item": page_item
    }

@register.simple_tag
def img_size_msg():
    return "حجم تصویر نباید بیشتر از ۲۰۰ کیلوبایت باشد"

@register.simple_tag
def none_img_tag():
    return format_html('<p><i class="fa-solid fa-square-xmark" style="font-size: 2rem;"></i></p><p>بدون تصویر</p>')
