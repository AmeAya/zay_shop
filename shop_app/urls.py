from django.urls import path
from .views import *

urlpatterns = [
    path('about_us', aboutUsView, name='about_us_url'),
    path('contact', contactView, name='contact_url'),
    path('products', productAllView, name='product_all_url'),
    path('product_detail/<int:product_id>', productDetailView, name='product_detail_url'),
    path('product_category/<int:category_id>', productByCategoryView, name='product_category_url'),
    path('products_gender/<int:gender_id>', productByGenderView, name='product_gender_url'),
    path('login', loginView, name='login_url'),
    path('logout', logoutView, name='logout_url'),
    path('registration', registerView, name='register_url'),
    path('profile', profileView, name='profile_url'),
    path('favourites', favouritesView, name='favourites_url'),
    path('history', historyView, name='history_url'),
    path('checkout', checkoutView, name='checkout_url'),
    path('buy', buyView, name='buy_url'),

    path('api/add_favourites', AddFavouritesApiView.as_view(), name='add_favourites_api_url'),
    path('api/add_cart', AddCartApiView.as_view(), name='cart_add'),
    path('api/category_by_gender', CategoryByGenderAPIView.as_view(), name='category_by_gender_api_url'),
    path('api/products_by_category', ProductsByCategoryAPIView.as_view(), name='products_by_category_api_url'),
    path('api/product_detail', ProductDetailAPIView.as_view(), name='product_detail_api_url'),

    path('', homeView, name='home_url'),
]

urlpatterns += [
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/', cart_detail, name='cart_detail'),
]
