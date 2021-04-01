from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='lili')
@stringfilter
def lili(value):
    text = value.replace('<p>', '<li>')
    text = text.replace('</p>', '</li>')
    return text


@register.filter(name='flexitem')
@stringfilter
def flexitem(value):
    text = value.replace('<p>', '<li><div class="flexListItem">')
    text = text.replace('</p>', '</div></li>')
    return text
