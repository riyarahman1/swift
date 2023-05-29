from django.core.paginator import Paginator
from django import template
register = template.Library()

@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=1, on_ends=1):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number, on_each_side=1, on_ends=1)