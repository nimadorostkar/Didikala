from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import requests
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse,JsonResponse
from datetime import datetime

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
from eshop_setting.models import SiteSetting



@login_required(login_url='/login')  # Check login
def ZarinpalGateway(request):
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
        data.save()

        order = Order.objects.get(id=data.id)
        authority = request.GET.get('Authority')

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount": totalPriceWithPost,
            "Description": "پرداخت هزینه خرید آنلاین",
            "Authority": authority,
            "CallbackURL": settings.ZARIN_CALL_BACK + str(order.code),
            "OrderID": order.code
        }
        data = json.dumps(data)

        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            response.raise_for_status()

            if response.status_code == 200:
                response = response.json()
                print('---------------')
                print(response)
                if response['Status'] == 100:
                    order.authority = response['Authority']
                    order.save()

                    redirect_url = settings.ZP_API_STARTPAY+str(response['Authority'])
                    return redirect(redirect_url)
                else:
                    return HttpResponse(response['errors'])
                    #return Response(response['errors'], status=400)
                    # return {'status': False, 'code': str(response['Status'])}
            #return response
            return HttpResponse(response)

        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}





@login_required(login_url='/login')
def PaymentVerify(request,ordercode):
    site_info = SiteSetting.objects.filter(status=True).first()
    current_user = request.user
    selected_post_way = PostWay.objects.get(selected=True)
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

    if request.method == 'GET':
        status = request.GET.get('Status')
        authority = request.GET.get('Authority')
        order = Order.objects.get(code=ordercode)

        context = {
            'site_info': site_info,
            'current_user': current_user,
            'shopcart': shopcart,
            'totalPrice': totalPrice,
            'totalCount': totalCount,
            'totalPriceWithPost': totalPriceWithPost,
            'order': order,
        }

        if not authority or status != "OK":
            order.delete()
            return render(request, 'order/shopping_notcomplete.html', context)


        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount": order.total,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:

                order.ref_id = response['RefID']
                order.paid = True
                order.save()
                for rs in shopcart:
                    detail = OrderProduct()
                    detail.order_id = order.id  # Order Id
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

                return render(request, 'order/shopping_complete.html', context)

            else:
                return SuccessResponse(data={'status': False, 'details': 'Subscription already paid'})
        return SuccessResponse(data=response.content)


