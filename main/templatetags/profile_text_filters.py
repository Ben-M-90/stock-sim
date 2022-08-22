from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def paragraph_truncate(value):
	paragraph_truncate = value.split('</p>', 1)
	if len(paragraph_truncate) == 0: return value
	paragraph_truncate = paragraph_truncate[0]
	paragraph_truncate.replace('<p>', '')
	paragraph_truncate.replace('</p>', '')
	return paragraph_truncate

@register.filter(is_safe=True)
@stringfilter
def paragraph_truncate_remainder(value):
	try:
		paragraph_truncate = value.split('</p>',1)
		if len(paragraph_truncate) == 0: return False
		paragraph_truncate = paragraph_truncate[1]
		paragraph_truncate.replace('<p>', '')
		paragraph_truncate.replace('</p>', '')
		return paragraph_truncate
	except:
		return value



