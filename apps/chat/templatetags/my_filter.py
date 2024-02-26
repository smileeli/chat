from django import template
register=template.Library()

def response(value):
    if value=="文心一言":
        return 1
    else:
        return 2


register.filter("response",response)