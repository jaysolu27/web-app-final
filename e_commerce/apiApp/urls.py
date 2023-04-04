from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/login/', views.userLoginView.as_view(), name='token_obtain_pair'),
    path('users/register/', views.registerView, name='register'),
    
    path('product-list-create/', views.ProductListCreateView.as_view(), name="product_api"),
    path('brand-list-create/', views.BrandListCreateView.as_view(), name="brand_api"),
    path('category-list-create/', views.CategoryListCreateView.as_view(), name="category_api"),
    path('user-list/', views.UserListView.as_view(), name="user_list_api"),
    path('top-products/', views.BestSellerView.as_view(), name="top_products"),
    path('seach-products/', views.SearchFilter.as_view(), name="top_products"),
    path('reviw-list/', views.ReviewDetailView.as_view(), name="review_list"),
    path('reviw-list/<int:user_id>/<int:product_id>/', views.ReviewDetailView.as_view(), name="review_list"),





    path('brand-detail-delete-update/<int:pk>/', views.BrandDetailUpdateDeleteView.as_view()),
    path('category-detail-delete-update/<int:pk>/', views.CategoryDetailUpdateDeleteView.as_view()),
    path('product-detail-delete-update/<int:pk>/', views.ProductDetailUpdateDeleteView.as_view()),

    path('product-filter/', views.ProductFilterView.as_view(), name="product_filter_view"),

    path('add-to-cart-api/', views.AddToCartApiView.as_view(), name='add_to_cart_api_view'),
    path('add-to-cart-api/<int:pk>/', views.AddToCartApiView.as_view(), name='add_to_cart_api_view'),

    path('create-order/<int:pk>/', views.CreateOrderView.as_view(), name='create_order_view'),
    path('create-order/', views.CreateOrderView.as_view(), name='create_order_view'),
    path('delete-cart/<int:pk>/', views.RemoveItemFromCart.as_view(), name='create_order_view'),


]

urlpatterns = format_suffix_patterns(urlpatterns)
