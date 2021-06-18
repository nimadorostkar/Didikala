from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from eshop_attribute.models import AttrProduct
from eshop_comment.forms import CommentForm, RateCommentForm
from eshop_comment.models import Comment, RateComment
from eshop_order.models import OrderProduct
from eshop_product.models import Product


@login_required(login_url='/login')
def comment_page(request, id):
    product = Product.objects.get_by_id(id)
    attrs = AttrProduct.objects.filter(product_id=id)
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        data = Comment()
        data.product = product
        data.subject = comment_form.cleaned_data['subject']
        data.comment = comment_form.cleaned_data['comment']
        ad = comment_form.cleaned_data['advantage']
        ad = ad.replace("'", '')
        ad = ad.replace("[", '')
        ad = ad.replace("]", '')
        data.advantage = ad
        dis = comment_form.cleaned_data['disadvantage']
        dis = dis.replace("'", '')
        dis = dis.replace("[", '')
        dis = dis.replace("]", '')
        data.disadvantage = dis
        data.advice = comment_form.cleaned_data['advice']
        data.ip = request.META.get('REMOTE_ADDR')
        current_user = request.user
        data.user_id = current_user
        # if some one buy that product before
        if OrderProduct.objects.filter(user_id=current_user, product_id=product).exists():
            data.order_product = OrderProduct.objects.filter(user_id=current_user, product_id=product).first()

        data.save()  # save data to table

        return HttpResponseRedirect('/')

    context = {
        'comment_form': comment_form,
        'product': product,
        'attrs': attrs,
        'product_attrs': product_attrs
    }
    return render(request, 'comment_product/comment.html', context)


def delete_comment(request, id):
    current_user = request.user
    url = request.META.get('HTTP_REFERER')  # get last url
    selected_comment = Comment.objects.get(user_id=current_user.id, id=id)
    selected_comment.delete()
    return HttpResponseRedirect(url)


def product_attrs(request, product_id, slug):
    url = request.META.get('HTTP_REFERER')  # get last url
    product_attr = RateCommentForm(request.POST or None)
    product = Product.objects.get(id=product_id)
    attr = AttrProduct.objects.get(slug__exact=slug, product__exact=product)
    if product_attr.is_valid():
        data = RateComment()
        data.attribute = attr
        data.rate = int(product_attr.cleaned_data['rate'])
        data.save()
        all_rate_comment = RateComment.objects.filter(attribute=attr).aggregate(avarage=Avg('rate'))
        avg = 0
        if all_rate_comment["avarage"] is not None:
            avg = int(all_rate_comment["avarage"])
            attr.rate = avg
            attr.save()
    return HttpResponseRedirect('/')


@login_required(login_url='/login')  # Check login
def comment_affective(request):
    url = request.META.get('HTTP_REFERER')  # get last url
    id = int(request.GET.get('commentid'))
    comment = Comment.objects.filter(id=id).first()
    result_notaf = ''
    result_af = ''
    if comment.notaffective.filter(id=request.user.id).exists():
        comment.notaffective.remove(request.user)
        comment.notaffective_count -= 1
        comment.affective.add(request.user)
        comment.affective_count += 1
        comment.save()
        result_af = comment.affective_count
        result_notaf = comment.notaffective_count

    if comment.affective.filter(id=request.user.id).exists():
        result_af = comment.affective_count
        result_notaf = comment.notaffective_count

    else:
        comment.affective.add(request.user)
        comment.affective_count += 1
        comment.save()
        result_af = comment.affective_count
        result_notaf = comment.notaffective_count

    return JsonResponse({'result_notaf': result_notaf, 'result_af': result_af})


@login_required(login_url='/login')  # Check login
def comment_notaffective(request):
    url = request.META.get('HTTP_REFERER')  # get last url
    id = int(request.GET.get('commentid'))
    comment = Comment.objects.filter(id=id).first()
    result_notaf = ''
    result_af = ''
    if comment.affective.filter(id=request.user.id).exists():
        comment.affective.remove(request.user)
        comment.affective_count -= 1

        comment.notaffective.add(request.user)
        comment.notaffective_count += 1
        comment.save()
        result_af = comment.affective_count
        result_notaf = comment.notaffective_count

    if comment.notaffective.filter(id=request.user.id).exists():
        result_af = comment.affective_count
        result_notaf = comment.notaffective_count
    else:
        comment.notaffective.add(request.user)
        comment.notaffective_count += 1
        comment.save()
        result_af = comment.affective_count
        result_notaf = comment.notaffective_count

    return JsonResponse({'result_notaf': result_notaf, 'result_af': result_af})
