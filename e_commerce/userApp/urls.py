from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from userApp import views

urlpatterns = [
    path('user-login/', views.UserLoginView.as_view(), name='login_page'),
    path('user-logout/', views.LogoutView.as_view(), name='logout_page'),
    path('about-us/', views.AboutUsView.as_view(), name='about_us'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us'),

    path('user-register/', views.UserRegisterView.as_view(), name='user_register'),
    path('', views.HomePageView.as_view(), name='home_page'),
    path('shop/', views.ShopPageView.as_view(), name='shop_page'),
    path('shop-details/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    path('add-to-cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart_view'),
    path('biling/', views.BilingVIew.as_view(), name='biling_view'),
    path('my-orders/', views.OrderHistoryView.as_view(), name='my_orders'),
    path('my-orders/<str:success>', views.OrderHistoryView.as_view(), name='my_orders_success'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
