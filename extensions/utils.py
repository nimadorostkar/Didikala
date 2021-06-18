from . import jalali
from django.utils import timezone


# convert english num to persian num
def persian_number_converter(mystr):
    number = {
        '1': '۱',
        '2': '۲',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹',
        '0': '۰',
    }
    for e, p in number.items():
        mystr = mystr.replace(e, p)
    return mystr


# convert english time to persian time and calender
def jalali_converter(time):
    jmonth = ['فرودین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند', ]
    time = timezone.localtime(time)
    time_to_string = '{},{},{}'.format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_string).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = '{} {} {} ، ساعت {}:{}'.format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.hour,
        time.minute,

    )
    return persian_number_converter(output)
