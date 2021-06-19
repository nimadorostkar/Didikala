from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.utils.crypto import get_random_string

from eshop_account.models import UserProfile, UserAddress
from eshop_category.models import Category
from eshop_order.forms import ShopCartForm, PostWayForm, PayWayForm
from eshop_order.models import ShopCart, Order, OrderProduct, PostWay
from eshop_product.models import Product
from eshop_variant.models import Variants


@login_required(login_url='/login')  # Check login
def addtoshopcart(request, id, variantid):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Product.objects.get(pk=id)
    variants = Variants.objects.filter(product_id=id, status='True')

    if product.variant != 'None' and variantid != 0:
        checkinvariant = ShopCart.objects.filter(variant_id=variantid,
                                                 user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id)  # Check product in shopcart
        if checkinproduct:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                if product.variant == 'None' or variantid == 0:
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                if form.cleaned_data['quantity']:
                    data.quantity = form.cleaned_data['quantity']
                else:
                    data.quantity += 1
                data.save()  # save data
            else:  # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                if product.variant == 'None' or variantid == 0:
                    data.variant_id = None
                else:
                    data.variant_id = variantid
                if form.cleaned_data['quantity']:
                    data.quantity = form.cleaned_data['quantity']
                else:
                    data.quantity = 1
                data.save()
        return redirect('ShopCart')

    else:  # if there is no post and after login request
        if control == 1:  # Update  shopcart
            if product.variant == 'None' or variantid == 0:
                data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            else:
                data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
            data.quantity += 1
            data.save()

        else:  # Insert to Shopcart
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            if product.variant != 'None' and variantid != 0:
                data.variant_id = variantid
            else:
                data.variant_id = None
            data.quantity = 1
            data.save()
        return redirect('ShopCart')


@login_required(login_url='/login')  # Check login
def removeshopcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    return redirect('ShopCart')


@login_required(login_url='/login')  # Check login
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    totalPrice = 0
    totalCount = 0
    for rs in shopcart:
        # check the variant is status active
        variants = Variants.objects.filter(product_id=rs.product_id, status='True')
        if rs.product.variant == 'None' or variants.count() == 0:
            totalPrice += rs.product.price * rs.quantity
            totalCount += rs.quantity
        else:
            totalPrice += rs.variant.price * rs.quantity
            totalCount += rs.quantity

    context = {'shopcart': shopcart,
               'category': category,
               'totalPrice': totalPrice,
               'totalCount': totalCount
               }
    return render(request, 'order/cart_list.html', context)


@login_required(login_url='/login')  # Check login
def shipping_page(request):
    current_user = request.user

    # find address and choose
    addresses = UserAddress.objects.filter(user__username=current_user)
    profile = UserProfile.objects.filter(user__username=current_user).first()
    selected_ad = UserAddress.objects.filter(user__username=current_user, selected=True).first()
    if len(addresses) > 0 and selected_ad == None:
        selected_ad = UserAddress.objects.filter(user__username=current_user).first()
        selected_ad.selected = True
        selected_ad.save()

    # find post way
    all_ways = PostWay.objects.all()
    selected_way = PostWay.objects.filter(selected=True).first()
    if selected_way is None:
        sel_way = PostWay.objects.get(way__contains='سریع')
        sel_way.selected = True
        sel_way.save()

    # find shop carts
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    totalPrice = 0
    totalPriceWithPost = 0
    totalCount = 0
    for rs in shopcart:
        # check the variant is status active
        variants = Variants.objects.filter(product_id=rs.product_id, status='True')
        if rs.product.variant == 'None' or variants.count() == 0:
            totalPrice += rs.product.price * rs.quantity
            totalPriceWithPost = totalPrice + (selected_way.price)
            totalCount += rs.quantity
        else:
            totalPrice += rs.variant.price * rs.quantity
            totalPriceWithPost = totalPrice + (selected_way.price)
            totalCount += rs.quantity

    context = {
        'current_user': current_user,
        'profile': profile,
        'addresses': addresses,
        'selected_ad': selected_ad,
        'shopcart': shopcart,
        'totalPrice': totalPrice,
        'totalCount': totalCount,
        'totalPriceWithPost': totalPriceWithPost,
        'all_ways': all_ways,
        'selected_way': selected_way
    }
    return render(request, 'order/shipping.html', context)


@login_required(login_url='/login')  # Check login
def way_selected(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    form = PostWayForm(request.POST)
    sl_way = PostWay.objects.get(id=id)
    if form.is_valid():
        sl_way.selected = True
        sl_way.save()
        other = PostWay.objects.all().exclude(id=id)
        for ad in other:
            ad.selected = False
            ad.save()
    return HttpResponseRedirect(url)


@login_required(login_url='/login')  # Check login
def pay_page(request):
    current_user = request.user

    # find address and choose
    selected_address = UserAddress.objects.get(user__username=current_user, selected=True)

    # find post way
    selected_post_way = PostWay.objects.get(selected=True)

    # find shop carts
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    totalPrice = 0
    totalCount = 0
    totalPriceWithPost = 0
    for rs in shopcart:
        # check the variant is status active
        variants = Variants.objects.filter(product_id=rs.product_id, status='True')
        if rs.product.variant == 'None' or variants.count() == 0:
            totalPrice += rs.product.price * rs.quantity
            totalPriceWithPost = totalPrice + selected_post_way.price
            totalCount += rs.quantity

        else:
            totalPrice += rs.variant.price * rs.quantity
            totalPriceWithPost = totalPrice + selected_post_way.price
            totalCount += rs.quantity

    forms = PayWayForm()
    context = {
        'current_user': current_user,
        'selected_address': selected_address,
        'shopcart': shopcart,
        'selected_post_way': selected_post_way,
        'totalPrice': totalPrice,
        'totalCount': totalCount,
        'totalPriceWithPost': totalPriceWithPost,
        'forms': forms
    }
    print(totalPriceWithPost)        # The total price we should to get
    return render(request, 'order/payment.html', context)



@login_required(login_url='/login')  # Check login
def order_completed(request):
    current_user = request.user

    # find address and choose
    selected_address = UserAddress.objects.get(user__username=current_user, selected=True)

    # find post way
    selected_post_way = PostWay.objects.get(selected=True)

    # find shop carts
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    totalPrice = 0
    totalCount = 0
    totalPriceWithPost = 0
    for rs in shopcart:
        # check the variant is status active
        variants = Variants.objects.filter(product_id=rs.product_id, status='True')
        if rs.product.variant == 'None' or variants.count() == 0:
            totalPrice += rs.product.price * rs.quantity
            totalPriceWithPost = totalPrice + selected_post_way.price
            totalCount += rs.quantity
        else:
            totalPrice += rs.variant.price * rs.quantity
            totalPriceWithPost = totalPrice + selected_post_way.price
            totalCount += rs.quantity

    if request.method == 'POST':  # if there is a post
        # return HttpResponse(request.POST.items())
        # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
        # ..............
        data = Order()
        data.user = request.user  # get product quantity from form
        data.address_address = selected_address.address
        data.address_full_name = selected_address.full_name
        data.address_phone = selected_address.phone
        data.address_ostsn = selected_address.ostan
        data.address_city = selected_address.city
        data.address_post_code = selected_address.post_code

        data.post_way = selected_post_way
        data.total = totalPriceWithPost
        data.amount = totalCount
        data.ip = request.META.get('REMOTE_ADDR')
        ordercode = get_random_string(10).upper()  # random cod
        data.code = ordercode
        data.save()  #
        for rs in shopcart:
            detail = OrderProduct()
            detail.order_id = data.id  # Order Id
            detail.product_id = rs.product_id
            detail.user_id = current_user.id
            detail.quantity = rs.quantity
            detail.amount = rs.amount

            # check the variant is status active
            variants = Variants.objects.filter(product_id=rs.product_id, status='True')
            if rs.product.variant == 'None' or variants.count() == 0:
                detail.price = rs.product.price
            else:
                detail.price = rs.variant.price
            detail.variant_id = rs.variant_id
            detail.save()

            if rs.product.variant == 'None' or variants.count() == 0:
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.all_sale += rs.quantity
                product.save()
            else:
                variant = Variants.objects.get(id=rs.variant_id)
                product = Product.objects.get(id=rs.product_id)
                variant.quantity -= rs.quantity
                product.all_sale += rs.quantity
                variant.save()
                product.save()

        ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
        request.session['cart_items'] = 0
        order = Order.objects.get(id=data.id)

    if request.method == 'GET':
        order = Order.objects.filter(user_id=current_user.id).last()

    context = {
        'current_user': current_user,
        'shopcart': shopcart,
        'totalPrice': totalPrice,
        'totalCount': totalCount,
        'totalPriceWithPost': totalPriceWithPost,
        'order': order,
    }
    return render(request, 'order/shopping_complete.html', context)
