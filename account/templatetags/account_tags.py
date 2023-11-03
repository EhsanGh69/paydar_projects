from django import template
from django.utils.translation import gettext_lazy as _


register = template.Library()


@register.filter
def index(iterable, index):
    return iterable[index]


@register.filter
def translate_names(name):
    permission_translate = [_(w).replace('Can', '').replace('add', 'افزودن').replace('change', 'ویرایش').replace('delete', 'حذف').replace('view', 'مشاهده') for w in (name).split()] # type: ignore
    return ' '.join(permission_translate)