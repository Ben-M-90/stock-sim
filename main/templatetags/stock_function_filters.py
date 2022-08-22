from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def get_shares_of_stock(ticker, portfolio):
	return portfolio.get_shares_of_stock(ticker)

@register.filter(is_safe=True)
@stringfilter
def get_shares_of_stock(ticker, portfolio):
	return portfolio.get_total_quantity_of_shares(ticker)