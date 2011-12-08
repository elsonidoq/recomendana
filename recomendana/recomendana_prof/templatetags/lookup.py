from django.template.defaultfilters import register
@register.filter(name='lookup')
def lookup(dict, index):
    if index in dict:
        return dict[index]
    try:
        i = int(index)
        if i in dict:
            return dict[i]
    except:
        return None
    return None
