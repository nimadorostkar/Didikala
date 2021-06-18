from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from eshop_setting.models import SiteSetting


# Create your views here.
from eshop_contact.forms import ContactUSForm
from eshop_contact.models import ContactMessage


# def contactus(request):
#     if request.method == 'POST':  # check post
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             data = ContactMessage()  # create relation with model
#             data.name = form.cleaned_data['name']  # get form input data
#             data.email = form.cleaned_data['email']
#             data.subject = form.cleaned_data['subject']
#             data.message = form.cleaned_data['message']
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()  # save data to table
#             messages.success(request, "Your message has ben sent. Thank you for your message.")
#             return HttpResponseRedirect('/contact')
#
#     form = ContactForm
#     context = {
#         'form': form
#     }
#     return render(request, 'contact_us.html', context)


def contact_page(request):
    contact_form = ContactUSForm(request.POST or None)
    site_info = SiteSetting.objects.filter(status=True).first()
    if contact_form.is_valid():
        name = contact_form.cleaned_data.get('name')
        email = contact_form.cleaned_data.get('email')
        subject = contact_form.cleaned_data.get('subject')
        message = contact_form.cleaned_data.get('message')
        ip = request.META.get('REMOTE_ADDR')
        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message, ip=ip)
        messages.success(request, "پیام شما با موفقیت ارسال شد")
        # todo: show user success massage
        contact_form = ContactUSForm()

    context = {
        'contact_form': contact_form,
        'site_info': site_info,
    }
    return render(request, 'contact_us/contact_us.html', context)
