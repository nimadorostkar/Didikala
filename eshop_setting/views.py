from django.shortcuts import render
from eshop_setting.models import FAQCategory, FAQ, SiteSetting


def faq_page(request):
    site_info = SiteSetting.objects.filter(status=True).first()
    faqCatList = FAQCategory.objects.filter(status='True')
    mostFaq = FAQ.objects.filter(mostAsked=True)
    context = {
        'faqCatList': faqCatList,
        'mostFaq': mostFaq,
        'site_info': site_info
    }
    return render(request, 'siteSetting/faq.html', context)


def faq_category(request, id):
    site_info = SiteSetting.objects.filter(status=True).first()
    faqCat = FAQCategory.objects.get(id=id, status='True')
    faqCatList = FAQ.objects.filter(category_id=id, status='True')
    mostFaq = FAQ.objects.filter(mostAsked=True)
    context = {
        'faqCat': faqCat,
        'faqCatList': faqCatList,
        'mostFaq': mostFaq,
        'site_info': site_info
    }
    return render(request, 'siteSetting/faq_category.html', context)


def faq_question(request, id):
    site_info = SiteSetting.objects.filter(status=True).first()
    mostFaq = FAQ.objects.filter(mostAsked=True)
    question = FAQ.objects.get(id=id, status='True')
    context = {
        'question': question,
        'mostFaq': mostFaq,
        'site_info': site_info
    }
    return render(request, 'siteSetting/faq.html', context)
