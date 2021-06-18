from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect, request, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, View
from eshop_comment.models import Comment
from eshop_order.models import Order, OrderProduct
from eshop_product.models import Product
from .forms import LoginForm, RegisterForm, UserAddressForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .models import UserProfile, UserAddress, History
from django.views.generic.detail import SingleObjectMixin


def login_user(request):
    url = request.META.get('HTTP_REFERER')  # get last url
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect to next page after login or home page
            request.session['variantid'] = request.POST
            return HttpResponseRedirect(request.GET.get('next', reverse('home')))
        else:
            form.add_error('username', 'نام کاربری یا رمز عبور اشتباه می‌باشد!!')
    return render(request, 'account/login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        password = register_form.cleaned_data.get('password')
        email = register_form.cleaned_data.get('email')
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        current_user = request.user
        data = UserProfile()
        data.user_id = current_user.id
        data.image = 'users/image/avatar.png'  # به طور پیش‌فرض این عکس رو برای همه میزاره
        data.save()
        return HttpResponseRedirect(request.GET.get('next', reverse('home')))
    context = {
        'register_form': register_form
    }
    return render(request, 'account/register.html', context)


def log_out(request):
    logout(request)
    return redirect('/')


# render partial
def product_slider(request):
    product_picked = Product.objects.filter(status=True).order_by('?')[:7]
    context = {
        'product_picked': product_picked
    }
    return render(request, 'account/_product_slider.html', context)


# render partial
def profile_sidebar(request):
    current_user = request.user.username
    profile = UserProfile.objects.filter(user__username=current_user).first()
    context = {
        'profile': profile,
    }
    return render(request, 'account/_profile_sidebar.html', context)


@login_required(login_url='/login')
def profile_page(request):
    current_user = request.user
    profile = UserProfile.objects.filter(user__username=current_user).first()
    orders = Order.objects.filter(user_id=current_user.id).order_by('-id')[:3]
    favourites = Product.objects.filter(favourite=request.user, status=True).order_by('-id')[:3]
    context = {
        'current_user': current_user,
        'profile': profile,
        'orders': orders,
        'favourites': favourites
    }
    return render(request, 'account/profile.html', context)


@login_required(login_url='/login')
def profile_info(request):
    current_user = request.user
    profile = UserProfile.objects.filter(user__username=current_user).first()
    context = {
        'current_user': current_user,
        'profile': profile,
    }
    return render(request, 'account/profile_info.html', context)


@login_required(login_url='/login')
def profile_info_edit(request):
    current_user = request.user
    profile = UserProfile.objects.filter(user__username=current_user).first()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form = user_form.save()
            profile_form = profile_form.save()
            return HttpResponseRedirect('/profile/info')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
            instance=request.user.profile)  # "userprofile" model -> OneToOneField relatinon with user

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'current_user': current_user,
            'profile': profile,
        }
        return render(request, 'account/profile_info_edit.html', context)


@login_required(login_url='/login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return HttpResponseRedirect('/profile')
        else:
            messages.error(request, 'لطفا ایرادات زیر را برطرف کنید.<br>' + str(form.errors))
            return HttpResponseRedirect('/profile/password')
    if request.method == 'GET':
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
        }
        return render(request, 'account/password_change.html', context)


def profile_addresses(request):
    current_user = request.user.username
    profile = UserProfile.objects.filter(user__username=current_user).first()
    addresses = UserAddress.objects.filter(user__username=current_user)
    context = {
        'current_user': current_user,
        'profile': profile,
        'addresses': addresses,
    }
    return render(request, 'account/address.html', context)


def add_address(request):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user.username
    form_ad = UserAddressForm(request.POST)
    if form_ad.is_valid():
        new_address = UserAddress()
        new_address.user_id = request.user.id
        new_address.full_name = form_ad.cleaned_data['full_name']
        new_address.phone = form_ad.cleaned_data['phone']
        new_address.ostan = form_ad.cleaned_data['ostan']
        new_address.city = form_ad.cleaned_data['city']
        new_address.address = form_ad.cleaned_data['address']
        new_address.post_code = form_ad.cleaned_data['post_code']
        new_address.selected = True
        new_address.save()
        other = UserAddress.objects.filter(user__username=current_user).exclude(id=new_address.id)
        for ad in other:
            ad.selected = False
            ad.save()
    return HttpResponseRedirect(url)


def edit_address(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    addresses = UserAddress.objects.get(id=id)
    current_user = request.user.username
    form_ad = UserAddressForm(request.POST)
    if form_ad.is_valid():
        addresses.full_name = form_ad.cleaned_data['full_name']
        addresses.phone = form_ad.cleaned_data['phone']
        addresses.ostan = form_ad.cleaned_data['ostan']
        addresses.city = form_ad.cleaned_data['city']
        addresses.address = form_ad.cleaned_data['address']
        addresses.post_code = form_ad.cleaned_data['post_code']
        addresses.selected = True
        addresses.save()
        other = UserAddress.objects.filter(user__username=current_user).exclude(id=id)
        for ad in other:
            ad.selected = False
            ad.save()
    return HttpResponseRedirect(url)


def remove_address(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    UserAddress.objects.filter(id=id).delete()
    return HttpResponseRedirect(url)


def selected_address(request, id):
    current_user = request.user.username
    url = request.META.get('HTTP_REFERER')  # get last url
    addresses = UserAddress.objects.get(id=id)
    form_ad = UserAddressForm(request.POST)
    if form_ad.is_valid():
        addresses.selected = True
        addresses.save()
        other = UserAddress.objects.filter(user__username=current_user).exclude(id=id)
        for ad in other:
            ad.selected = False
            ad.save()

    return HttpResponseRedirect(url)


class OrdersList(ListView):
    template_name = 'account/profile-orders.html'
    paginate_by = 30

    def get_queryset(self):
        request = self.request
        current_user = request.user
        orders = Order.objects.filter(user_id=current_user.id)
        return orders

    def get_context_data(self, *, object_list=None, **kwargs):
        request = self.request
        current_user = request.user
        profile = UserProfile.objects.filter(user__username=current_user).first()
        orders = Order.objects.filter(user_id=current_user.id).order_by("-id")
        context = {
            'profile': profile,
            'orders': orders
        }
        return context


def order_detail(request, id):
    order = Order.objects.get(id=id)
    if order.status == 'Canceled':
        num = 0
    if order.status == 'New':
        num = 1
    if order.status == 'Accepted':
        num = 2
    if order.status == 'Preparing':
        num = 3
    if order.status == 'OutCompany':
        num = 4
    if order.status == 'InPostOffice':
        num = 5
    if order.status == 'OnShipping':
        num = 6
    if order.status == 'Arrive':
        num = 7
    current_user = request.user
    profile = UserProfile.objects.filter(user__username=current_user).first()

    products = OrderProduct.objects.filter(order_id=order.id)

    context = {
        'order': order,
        'profile': profile,
        'num': num,
        'products': products,

    }
    return render(request, 'account/profile_order_detail.html', context)


class CommentsList(ListView):
    template_name = 'account/profile_comments.html'
    paginate_by = 2

    def get_queryset(self):
        request = self.request
        current_user = request.user
        comments = Comment.objects.filter(user_id=current_user.id)
        return comments

    def get_context_data(self, *, object_list=None, **kwargs):
        request = self.request
        current_user = request.user
        profile = UserProfile.objects.filter(user__username=current_user).first()
        comments = Comment.objects.filter(user_id=current_user.id, product__status=True, ).order_by('-id')
        context = {
            'profile': profile,
            'comments': comments
        }
        return context


class HistoryList(ListView):
    template_name = 'account/profile_user_history.html'

    def get_queryset(self):
        request = self.request
        current_user = request.user
        user_history = History.objects.filter(user_id=current_user.id)
        return user_history

    def get_context_data(self, *, object_list=None, **kwargs):
        request = self.request
        current_user = request.user
        user_history = History.objects.filter(user_id=current_user.id).order_by('-id')[:20]

        # find the product details from history
        history_list = []
        for history in user_history:
            name = history.content_object
            product = Product.objects.get(title__exact=name)
            if product.status == 'True':
                history_list.append(product)

        # remove duplicate items from history list
        history_list = list(dict.fromkeys(history_list))

        context = {
            'history_list': history_list,
            'user_history': user_history
        }
        return context


def history_delete(request, id):
    histories = History.objects.filter(object_id__exact=id, user_id=request.user.id)
    # we find history with product id and user id
    # maybe one product seen more than once than we should delete all same product
    for history in histories:
        history.delete()
    return redirect('historyList')


@login_required(login_url='/login')  # Check login
def product_favourite(request, product_id):
    url = request.META.get('HTTP_REFERER')  # get last url
    product = Product.objects.get_by_id(product_id)
    absolute = product.get_absolute_url

    if url == absolute:
        result = ''
        if product.favourite.filter(id=request.user.id).exists():
            product.favourite.remove(request.user)
            result += ''
        else:
            product.favourite.add(request.user)
            result = 'favorites'

        return JsonResponse({'result': result, })
    else:
        if product.favourite.filter(id=request.user.id).exists():
            product.favourite.remove(request.user)
        else:
            product.favourite.add(request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def profile_favourites(request):
    current_user = request.user.username
    favourites = Product.objects.filter(favourite=request.user, status=True)
    context = {
        'current_user': current_user,
        'favourites': favourites,
    }
    return render(request, 'account/profile_favourites.html', context)
