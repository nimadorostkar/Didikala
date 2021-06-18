from django.shortcuts import render

# Create your views here.
from eshop_setting.models import FAQCategory, FAQ


def faq_page(request):
    faqCatList = FAQCategory.objects.filter(status='True')
    mostFaq = FAQ.objects.filter(mostAsked=True)
    context = {
        'faqCatList': faqCatList,
        'mostFaq': mostFaq,
    }
    return render(request, 'siteSetting/faq.html', context)


def faq_category(request, id):
    faqCat = FAQCategory.objects.get(id=id, status='True')
    faqCatList = FAQ.objects.filter(category_id=id, status='True')
    mostFaq = FAQ.objects.filter(mostAsked=True)
    context = {
        'faqCat': faqCat,
        'faqCatList': faqCatList,
        'mostFaq': mostFaq,
    }
    return render(request, 'siteSetting/faq_category.html', context)


def faq_question(request, id):
    mostFaq = FAQ.objects.filter(mostAsked=True)
    question = FAQ.objects.get(id=id, status='True')
    context = {
        'question': question,
        'mostFaq': mostFaq,
    }
    return render(request, 'siteSetting/faq.html', context)
