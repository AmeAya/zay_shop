from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from cart.cart import Cart

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import *
from .serializers import *


def homeView(request):
    genders = Gender.objects.all()
    categories = Category.objects.filter(popular=True)[:3]
    popular_products = Product.objects.filter(popular=True)[:3]
    context = {
        'categories': categories,
        'genders': genders,
        'popular_products': popular_products
    }
    return render(request, 'index.html', context=context)


def registerView(request):
    if request.user.is_authenticated:
        return redirect('home_url')

    if request.method == 'GET':
        genders = Gender.objects.all()
        categories = Category.objects.filter(popular=True)[:3]
        popular_products = Product.objects.filter(popular=True)[:3]
        context = {
            'categories': categories,
            'genders': genders,
            'popular_products': popular_products,
            'error': request.session.get('error')
        }
        return render(request, template_name='register.html', context=context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(CustomUser.objects.filter(email=email)) > 0:
            request.session.update({'error': 'This email already taken!'})
            return redirect('register_url')
        if 'error' in request.session.keys():
            del request.session['error']
        user = CustomUser.objects.create_user(email=email, password=password)
        login(request, user)
        return redirect('profile_url')


def favouritesView(request):
    if request.user.is_authenticated:
        genders = Gender.objects.all()
        products = request.user.favourites.all()

        paginator = Paginator(products, 9)
        page_num = request.GET.get('page')
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_num = 1
            page_obj = paginator.page(1)
        except EmptyPage:
            page_num = paginator.num_pages
            page_obj = paginator.page(paginator.num_pages)

        pages = []
        for i in range(1, paginator.num_pages + 1):
            if i == page_num:
                pages.append({
                    'num': i,
                    'url': 'product_all_url',
                    'active': 'active'
                })
            else:
                pages.append({
                    'num': i,
                    'url': 'product_all_url',
                    'active': ''
                })

        context = {
            'pages': pages,
            'products': page_obj,
            'genders': genders
        }
        return render(request, template_name='shop.html', context=context)
    return redirect('login_url')


def historyView(request):
    if not request.user.is_authenticated:
        return redirect('login_url')
    genders = Gender.objects.all()
    categories = Category.objects.filter(popular=True)[:3]
    popular_products = Product.objects.filter(popular=True)[:3]
    orders = Order.objects.filter(customer=request.user)
    context = {
        'categories': categories,
        'genders': genders,
        'popular_products': popular_products,
        'orders': orders
    }
    return render(request, template_name='history.html', context=context)


def checkoutView(request):
    genders = Gender.objects.all()
    categories = Category.objects.filter(popular=True)[:3]
    popular_products = Product.objects.filter(popular=True)[:3]
    cart = Cart(request).cart
    total = 0
    for key, value in cart.items():
        total += int(value.get('price'))

    context = {
        'categories': categories,
        'genders': genders,
        'popular_products': popular_products,
        'total': total
    }
    return render(request, template_name='checkout.html', context=context)


def buyView(request):
    if not request.user.is_authenticated:
        return redirect('login_url')

    cart = Cart(request).cart
    total = 0
    order = Order(customer=request.user, total=total, status='Accepted')
    order.save()
    for key, value in cart.items():
        product = Product.objects.get(id=key)
        quantity = int(value.get('quantity'))
        item = OrderItem(product=product, quantity=quantity, total=int(product.price) * quantity)
        item.save()
        order.items.add(item)
        order.save()
        total += int(value.get('price'))
    order.total = total
    order.save()
    cart.clear()
    return redirect('profile_url')


def profileView(request):
    if request.user.is_authenticated:
        genders = Gender.objects.all()
        categories = Category.objects.filter(popular=True)[:3]
        popular_products = Product.objects.filter(popular=True)[:3]
        context = {
            'categories': categories,
            'genders': genders,
            'popular_products': popular_products
        }
        return render(request, template_name='profile.html', context=context)
    return redirect('login_url')


def loginView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('profile_url')
        genders = Gender.objects.all()
        categories = Category.objects.filter(popular=True)[:3]
        popular_products = Product.objects.filter(popular=True)[:3]
        context = {
            'categories': categories,
            'genders': genders,
            'popular_products': popular_products,
            'error': request.session.get('error')
        }
        return render(request, template_name='login.html', context=context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            if 'error' in request.session.keys():
                del request.session['error']
            return redirect('profile_url')
        else:
            request.session.update({'error': 'Email and/or password incorrect. Try again'})
            return redirect('login_url')


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home_url')


def aboutUsView(request):
    genders = Gender.objects.all()
    categories = Category.objects.filter(popular=True)[:3]
    popular_products = Product.objects.filter(popular=True)[:3]
    brands = Brand.objects.all()

    paginator = Paginator(brands, 4)
    brand_list = []
    for i in range(paginator.num_pages):
        elem = {
            'num': i + 1,
            'brands': paginator.page(i + 1)
        }
        brand_list.append(elem)

    context = {
        'categories': categories,
        'genders': genders,
        'popular_products': popular_products,
        'brand_list': brand_list
    }
    return render(request, 'about.html', context=context)


def contactView(request):
    genders = Gender.objects.all()
    categories = Category.objects.filter(popular=True)[:3]
    popular_products = Product.objects.filter(popular=True)[:3]
    context = {
        'categories': categories,
        'genders': genders,
        'popular_products': popular_products
    }
    return render(request, 'contact.html', context=context)


def productDetailView(request, product_id):
    product = Product.objects.get(id=product_id)
    paginator = Paginator(product.images.all(), 3)
    image_list = []
    for i in range(paginator.num_pages):
        elem = {
            'num': i + 1,
            'images': paginator.page(i + 1)
        }
        image_list.append(elem)

    context = {
        'product': product,
        'image_list': image_list
    }
    return render(request, 'shop-single.html', context=context)


def productAllView(request):
    genders = Gender.objects.all()
    products = Product.objects.all()

    paginator = Paginator(products, 9)
    page_num = request.GET.get('page')
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_num = 1
        page_obj = paginator.page(1)
    except EmptyPage:
        page_num = paginator.num_pages
        page_obj = paginator.page(paginator.num_pages)

    pages = []
    for i in range(1, paginator.num_pages + 1):
        if i == page_num:
            pages.append({
                'num': i,
                'url': 'product_all_url',
                'active': 'active'
            })
        else:
            pages.append({
                'num': i,
                'url': 'product_all_url',
                'active': ''
            })

    context = {
        'pages': pages,
        'products': page_obj,
        'genders': genders
    }

    return render(request, 'shop.html', context=context)


def productByCategoryView(request, category_id):
    genders = Gender.objects.all()
    category = Category.objects.get(id=category_id)
    categories = Category.objects.filter(gender=category.gender)
    products = Product.objects.filter(category=category)

    paginator = Paginator(products, 9)
    page_num = request.GET.get('page')
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_num = 1
        page_obj = paginator.page(1)
    except EmptyPage:
        page_num = paginator.num_pages
        page_obj = paginator.page(paginator.num_pages)

    pages = []
    for i in range(1, paginator.num_pages + 1):
        if i == page_num:
            pages.append({
                'num': i,
                'url': 'product_category_url',
                'active': 'active'
            })
        else:
            pages.append({
                'num': i,
                'url': 'product_category_url',
                'active': ''
            })

    context = {
        'pages': pages,
        'products': page_obj,
        'categories': categories,
        'selected': category_id,
        'genders': genders
    }

    return render(request, 'shop.html', context=context)


def productByGenderView(request, gender_id):
    genders = Gender.objects.all()
    gender = Gender.objects.get(id=gender_id)
    categories = Category.objects.filter(gender=gender)
    products = Product.objects.filter(gender=gender)

    paginator = Paginator(products, 9)
    page_num = request.GET.get('page')
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_num = 1
        page_obj = paginator.page(1)
    except EmptyPage:
        page_num = paginator.num_pages
        page_obj = paginator.page(paginator.num_pages)

    pages = []
    for i in range(1, paginator.num_pages + 1):
        if i == page_num:
            pages.append({
                'num': i,
                'url': 'product_gender_url',
                'active': 'active'
            })
        else:
            pages.append({
                'num': i,
                'url': 'product_gender_url',
                'active': ''
            })

    context = {
        'pages': pages,
        'products': page_obj,
        'categories': categories,
        'genders': genders,
        'selected': gender_id
    }

    return render(request, 'shop.html', context=context)


@login_required(login_url="login_url")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login_url")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login_url")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login_url")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login_url")
def cart_detail(request):
    cart = Cart(request)
    links = [
        {'name': 'home', 'url': 'home_url', 'active': ''},
        {'name': 'men', 'url': 'men_url', 'active': ''},
        {'name': 'women', 'url': 'women_url', 'active': ''},
        {'name': 'kid', 'url': 'kid_url', 'active': ''},
        {'name': 'accessories', 'url': 'accessories_url', 'active': ''},
        {'name': 'about', 'url': 'about_url', 'active': ''},
        {'name': 'contact us', 'url': 'contact_url', 'active': ''},
        {'name': 'profile', 'url': 'profile_url', 'active': ''},
        {'name': 'logout', 'url': 'logout_url', 'active': ''},
    ]

    total = 0
    for key, value in cart.cart.items():
        total += int(value.get('price'))

    context = {
        'links': links,
        'total': total
    }
    return render(request, template_name='cart_detail.html', context=context)


class AddFavouritesApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        if request.user.is_authenticated:
            product_id = request.data.get('product_id').split('_')[-1]
            if product_id is None or product_id == '':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            product = Product.objects.get(id=product_id)
            if product in request.user.favourites.all():
                request.user.favourites.remove(product)
            else:
                request.user.favourites.add(product)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AddCartApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        if request.user.is_authenticated:
            cart = Cart(request)
            product_id = request.data.get('product_id').split('_')[-1]

            if product_id is None or product_id == '':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            product = Product.objects.get(id=product_id)

            for key, value in cart.cart.items():
                if product_id == value.get('product_id'):
                    break
            else:
                cart.add(product=product)
                return Response(status=status.HTTP_200_OK)

            cart.remove(product=product)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoryByGenderAPIView(APIView):
    permission_classes = []

    def get(self, request):
        gender = Gender.objects.get(id=request.GET.get('id'))
        categories = Category.objects.filter(gender=gender)
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class ProductsByCategoryAPIView(APIView):
    permission_classes = []

    def get(self, request):
        category = Category.objects.get(id=request.GET.get('id'))
        products = Product.objects.filter(category=category)
        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class ProductDetailAPIView(APIView):
    permission_classes = []

    def get(self, request):
        product = Product.objects.get(id=request.GET.get('id'))
        data = ProductSerializer(product, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)
