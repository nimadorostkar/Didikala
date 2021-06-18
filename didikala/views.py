import itertools
from django.shortcuts import render, redirect

# header code behind
from eshop_brand.models import Brand
from eshop_category.models import Category
from eshop_order.models import ShopCart
from eshop_product.models import Product
from eshop_setting.models import SiteSetting
from eshop_slider.models import Slider
from eshop_variant.models import Variants


def header(request, *args, **kwargs):
    category = Category.objects.filter(status=True)
    ancestors = category.get_ancestors()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    totalPrice = 0
    totalCount = 0
    for rs in shopcart:
        variants = Variants.objects.filter(product_id=rs.product_id, status='True')
        if rs.product.variant == 'None' or variants.count() == 0:

            totalPrice += rs.product.price * rs.quantity
            totalCount += rs.quantity
        else:
            totalPrice += rs.variant.price * rs.quantity
            totalCount += rs.quantity

    context = {
        'category': category,
        'ancestors': ancestors,
        'shopcart': shopcart,
        'totalPrice': totalPrice,
        'totalCount': totalCount
    }
    return render(request, 'shared/Header.html', context)


# footer code behind
def footer(request, *args, **kwargs):
    site_info = SiteSetting.objects.filter(status=True).first()
    context = {
        'site_info': site_info
    }

    return render(request, 'shared/Footer.html', context)


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def home_page(request):
    sliders = Slider.objects.all()
    product_all_sale = Product.objects.filter(category__in=Category.objects.get(slug='digital-product') \
                                              .get_descendants(include_self=True), status=True).order_by('-all_sale')[:7]
    product_latest = Product.objects.filter(status=True).order_by('-id')[:7]
    # product_all_sale = Product.objects.all().order_by('all_sale')[:7]
    product_picked = Product.objects.filter(status=True).order_by('?')[:7]
    product_group = Product.objects.filter(status=True).order_by('?')[:9]
    grouped_product = list(my_grouper(3, product_group))
    all_barand = Brand.objects.all()
    context = {
        'sliders': sliders,
        'product_latest': product_latest,
        'product_picked': product_picked,
        'grouped_product': grouped_product,
        'product_all_sale': product_all_sale,
        'all_barand': all_barand,
    }
    return render(request, 'home_page.html', context)
