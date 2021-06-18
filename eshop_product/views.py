import itertools
import json

from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseNotFound
from django.template.loader import render_to_string

from eshop_attribute.models import AttrProduct
from eshop_brand.models import Brand
from eshop_category.models import Category
from eshop_comment.models import Comment
from eshop_account.signals import object_viewed_signal  # record product view in history
from eshop_image.models import Images
from eshop_product.filter import ProductFilter
from eshop_product.models import Product
from django.core.paginator import Paginator

from eshop_tag.models import Tag
from eshop_variant.models import Variants


def search_list(request):
    query = request.GET.get('q')
    products = Product.objects.search(query)

    colors_list = []
    brand_list = []
    sizes_list = []
    child_list = []

    for pro in products:
        child_list.append(pro.category)
        brand_list.append(pro.brand)
        if pro.variant == 'Color':
            var = Variants.objects.filter(product_id=pro.id)
            for v in var:
                color = v.color
                colors_list.append(color)
        if pro.variant == 'Size':
            var = Variants.objects.filter(product_id=pro.id)
            for v in var:
                size = v.size
                sizes_list.append(size)
        if pro.variant == 'Size-Color':
            var = Variants.objects.filter(product_id=pro.id)
            for v in var:
                size = v.size
                color = v.color
                sizes_list.append(size)
                colors_list.append(color)

    colors = [i for n, i in enumerate(colors_list) if i not in colors_list[n + 1:]]
    sizes = [i for n, i in enumerate(sizes_list) if i not in sizes_list[n + 1:]]
    brands = [i for n, i in enumerate(brand_list) if i not in brand_list[n + 1:]]
    childs = [i for n, i in enumerate(child_list) if i not in child_list[n + 1:]]

    my_filter = ProductFilter(request.GET, queryset=products)
    products = my_filter.qs

    paginator = Paginator(products, 8)  # Show 8 product per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'colors': colors,
        'brands': brands,
        'sizes': sizes,
        'childs': childs

    }
    return render(request, 'product/product_list.html', context)


# ارسال ajax به سرچ باکس و ویویی که در بالا نوشته شده
def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Tag.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)

        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)


def product_list_category(request, slug):
    if slug == 'New':
        # from home page
        products = Product.objects.get_active_product().order_by('-id')
        childs = Category.objects.all()
    else:
        products = Product.objects.get_by_categories(slug)
        category = Category.objects.get(slug=slug, status=True)
        children_cat = category.get_children()
        childs = []
        for child in children_cat:
            if child.status == 'True':
                childs.append(child)

    colors_list = []
    brand_list = []
    sizes_list = []

    for pro in products:
        if pro.brand != None:
            brand_list.append(pro.brand)
        if pro.variant == 'Color':
            var = Variants.objects.filter(product_id=pro.id)
            for v in var:
                color = v.color
                colors_list.append(color)
        if pro.variant == 'Size':
            var = Variants.objects.filter(product_id=pro.id)
            for v in var:
                size = v.size
                sizes_list.append(size)
        if pro.variant == 'Size-Color':
            var = Variants.objects.filter(product_id=pro.id)
            for v in var:
                size = v.size
                color = v.color
                sizes_list.append(size)
                colors_list.append(color)

    colors = [i for n, i in enumerate(colors_list) if i not in colors_list[n + 1:]]
    sizes = [i for n, i in enumerate(sizes_list) if i not in sizes_list[n + 1:]]
    brands = [i for n, i in enumerate(brand_list) if i not in brand_list[n + 1:]]

    # filter for sidebar
    my_filter = ProductFilter(request.GET, queryset=products)
    products = my_filter.qs

    paginator = Paginator(products, 8)  # Show 8 product per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'childs': childs,
        'colors': colors,
        'sizes': sizes,
        'brands': brands,
        'my_filter': my_filter,
        'slug': slug
    }

    return render(request, 'product/product_list.html', context)


def product_list_brand(request, slug):
    products = Product.objects.filter(brand__in=Brand.objects.filter(slug=slug), status=True)
    colors_list = []
    sizes_list = []
    brand_list = []
    child_list = []
    for pro in products:
        child_list.append(pro.category)
        if pro.variant == 'Color':
            var = Variants.objects.filter(product_id=pro.id)
            for v in var:
                color = v.color
                colors_list.append(color)
        if pro.variant == 'Size':
            var = Variants.objects.filter(product_id=pro.id)
            for v in var:
                size = v.size
                sizes_list.append(size)
        if pro.variant == 'Size-Color':
            var = Variants.objects.filter(product_id=pro.id)
            for v in var:
                size = v.size
                color = v.color
                sizes_list.append(size)
                colors_list.append(color)

    colors = [i for n, i in enumerate(colors_list) if i not in colors_list[n + 1:]]
    sizes = [i for n, i in enumerate(sizes_list) if i not in sizes_list[n + 1:]]
    brands = [i for n, i in enumerate(brand_list) if i not in brand_list[n + 1:]]
    childs = [i for n, i in enumerate(child_list) if i not in child_list[n + 1:]]

    # filter for sidebar
    my_filter = ProductFilter(request.GET, queryset=products)
    products = my_filter.qs

    paginator = Paginator(products, 8)  # Show 8 product per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'childs': childs,
        'colors': colors,
        'sizes': sizes,
        'brands': brands,
        'my_filter': my_filter,
        'slug': slug
    }

    return render(request, 'product/product_list.html', context)


# list group for gallery
def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def product_detail(request, product_id, slug):
    query = request.GET.get('qv')
    product = Product.objects.get_by_id(product_id)
    if product == None:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    # for each view, add 1 view count to product views
    product.view_count += 1
    product.save()

    # for FBV i use this code on the function view directly
    #  add this code to record product view in history of users profile
    if request.user.is_authenticated:
        object_viewed_signal.send(product.__class__, instance=product, request=request)

    cat = product.category.parent

    if product is None or not product.status:
        raise Http404('محصول مورد نظر یافت نشد!!')

    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    product_gallery = Images.objects.filter(product_id=product_id)
    tags = product.tag_set.all()
    related_product = Product.objects.filter(category__in=Category.objects.get(title=cat) \
                                             .get_descendants(include_self=True)).exclude(id=product.id)
    product_comments = Comment.objects.filter(product_id=product, status='Submit').order_by('-id')
    product_attr = AttrProduct.objects.filter(product_id=product_id)
    context = {
        'product': product,
        'tags': tags,
        'related_product': related_product,
        'product_gallery': product_gallery,
        'product_comments': product_comments,
        'product_attr': product_attr,
        'is_favourite': is_favourite,
        'cat': cat
    }
    if product.variant != "None":  # Product have variants
        variants = Variants.objects.filter(product_id=product_id, status='True')
        if variants.count() != 0:
            if request.method == 'POST':  # if we select color
                variant_id = request.POST.get('variantid')
                variant = Variants.objects.get(id=variant_id, status='True')  # selected product by click color radio
                colors = Variants.objects.filter(product_id=product_id, size_id=variant.size_id, status='True')
                sizes = Variants.objects.raw(
                    'SELECT * FROM   eshop_variant_variants   WHERE product_id=%s AND status=%s GROUP BY size_id',
                    [product_id, 'True'])
                query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color) + 'status:"True"'
            else:
                variants = Variants.objects.filter(product_id=product_id, status='True')
                colors = Variants.objects.filter(product_id=product_id, size_id=variants[0].size_id, status='True')
                sizes = Variants.objects.raw(
                    'SELECT * FROM  eshop_variant_variants  WHERE product_id=%s AND status=%s GROUP BY size_id',
                    [product_id, 'True'])
                variant = Variants.objects.get(id=variants[0].id, status='True')

            context.update(
                {'sizes': sizes,
                 'colors': colors,
                 'variant': variant,
                 'query': query,
                 'variants': variants
                 })

    return render(request, 'product/product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id, status='True')
        if colors.count() == 0:
            colors = None
        product = Product.objects.get_by_id(productid)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
            'product': product
        }
        data = {'rendered_table': render_to_string('product/color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)
