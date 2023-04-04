from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.DashBoardView.as_view()),
    path('dashboard/', views.DashBoardView.as_view(), name='dashboard_name'),
    path('brand/', views.BrandView.as_view(), name='brand_name'),
    path('category/', views.CategoryView.as_view(), name='category_name'),
    path('product/', views.ProductView.as_view(), name='product_name'),
    path('user-lst/', views.UserListView.as_view(), name='user_lst'),
    path('view-order/', views.OrderListView.as_view(), name='view_order'),



    # path('shop/', views.ShopPageView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
