from django import template

register = template.Library()


@register.filter(name='split')
def split(value, key):
    """
      Returns the value turned into a list.
    """
    return value.split(key)


@register.simple_tag
def my_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.simple_tag
def order_url(value, field_name, urlencode=None):
    url = '{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')

        # if page was more than 1 we should delete it to start it from page=1
        for item in querystring:
            if item.find("page") > -1:
                querystring.remove(item)

        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '?page=1&{}&{}'.format(encoded_querystring, url)
    else:
        url = '?page=1s=&{}'.format(url)
    return url


@register.filter(name='check_url')
def check_url(value, field_name):
    url = '{}={}&'.format(value, field_name)
    return url
