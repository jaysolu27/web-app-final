from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from apiApp import models, serializers
from rest_framework import status
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from apiApp.serializers import getJWTTokenSerializer, UserSerializerWithToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from apiApp.constants import FILTER_KEYWORDS
####### User register page#####
# user login view with jwt token




class userLoginView(TokenObtainPairView):
    serializer_class = getJWTTokenSerializer


# user registration view
@api_view(["POST"])
def registerView(request):
    data = request.data
    if data["password"] != data["checkpassword"]:
        print("ehererere i amma")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if data["name"] and len(data["name"].split(" ")) == 2:
        user_obj = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name = data["name"].split(" ")[0],
            last_name = data["name"].split(" ")[1],
            password=make_password(data["password"]),
        )
    elif data["name"] and len(data["name"].split(" ")) >2:
        user_obj = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name = data["name"].split(" ")[-1],
            last_name = data["name"].split(" ")[0],
            password=make_password(data["password"]),
        )
    else:    
        user_obj = User.objects.create(
            username=data["username"],
            email=data["email"],
            first_name = data["name"],
            password=make_password(data["password"]),
        )
    serialized_data = UserSerializerWithToken(user_obj, many=False)
    if serialized_data.is_valid:
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)
    else:
        print(serialized_data.errors)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListCreateView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    permission_classes = [IsAuthenticated]
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            brand_obj = models.BrandModel.objects.filter(id=request.POST.get("brand_id"))
            category_obj = models.CategoryModel.objects.filter(id=request.POST.get("category_id"))

            product_obj = models.ProductModel.objects.create(
                p_name = request.POST.get("p_name"),
                p_desc = request.POST.get("p_desc"),
                p_price = request.POST.get("p_price"),
                brand_id = brand_obj,
                category_id = category_obj,
                p_img = request.FILES.get("p_img")
            )
        except Exception as e:
            tt = tt
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductFilterView(
    mixins.ListModelMixin, generics.GenericAPIView
):
    permission_classes = [IsAuthenticated]
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_filter_key(self, key, val):
        if type(val) == str and '-' in val:
            val1, val2 =  val.split('-')
            return {f"{key}__gte":val1, f"{key}__lte":val2}
        if type(val) == str:
            return {key:val}
        if type(val) == list:
            return {f"{key}__in": val}
        if key == "p_price" and val=="all-price":
            return {}


    def get_filter_params(self):
        filterset_fields = {}
        for key in self.request.POST:
            filterset_fields.update(self.get_filter_key(key, self.request.POST[key]))
        return filterset_fields
            

    def list(self, request, *args, **kwargs):
        queryset = models.ProductModel.objects.all()
        if request.POST:
            try:
                queryset = queryset.filter(**self.get_filter_params())
            except Exception as e:
                print(e)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class BrandListCreateView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    permission_classes = [IsAuthenticated]
    queryset = models.BrandModel.objects.all()
    serializer_class = serializers.BrandSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"data": serializer.data, "msg": "Brand Created Successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryListCreateView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    permission_classes = [IsAuthenticated]
    queryset = models.CategoryModel.objects.all()
    serializer_class = serializers.CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductDetailUpdateDeleteView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated]
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReviewDetailView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated]
    queryset = models.ReviewModel.objects.all()
    serializer_class = serializers.ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request,user_id=None, product_id=None, *args, **kwargs):
        res = models.ReviewModel.objects.filter(product_id=product_id).values("review", "user_id__username", 'user_id__id')
        return Response({'review_lst':res})
    
    def post(self, request, *args, **kwargs):
        review_obj = models.ReviewModel.objects.filter(
            user_id =request.POST.get("user_id"),
            product_id =  request.POST.get("product_id")   
            ).first()
        if review_obj:
            review_obj.review = request.POST.get("review")
            review_obj.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BrandDetailUpdateDeleteView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated]
    queryset = models.BrandModel.objects.all()
    serializer_class = serializers.BrandSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, pk, *args, **kwargs):
        tt="TT"
        return self.destroy(request, *args, **kwargs)


class CategoryDetailUpdateDeleteView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated]
    queryset = models.CategoryModel.objects.all()
    serializer_class = serializers.CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AddToCartApiView(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    generics.GenericAPIView,
    ):
    permission_classes = [IsAuthenticated]
    queryset = models.UserCart.objects.all()
    serializer_class = serializers.UserCartSerializer

    def list(self, request, pk, *args, **kwargs):
        cart_queryset = models.UserCart.objects.filter(user_id=pk).values(
            'product_id','product_count','id'
            )
        response_data = []
        total_cnt = 0
        total_cost = 0
        for ele in cart_queryset:
            temp = models.ProductModel.objects.filter(id=ele['product_id']).first()
            serializer = serializers.ProductSerializer(temp)
            temp_dict = {
                'cart_id':ele['id'],
                'name':temp.p_name, 
                'count':ele['product_count'], 
                'img':serializer.data['p_img'], 
                'price':temp.p_price*ele['product_count'],
                'og_price':temp.p_price,
                'product_id': ele['product_id']
                }
            response_data.append(temp_dict)
            total_cnt += ele['product_count']
            total_cost += temp.p_price*ele['product_count']
        return Response({'data':response_data, 'total_cnt':total_cnt, 'total_cost':total_cost})


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

    def update(self, request, *args, **kwargs):
        query = models.UserCart.objects.filter(
            user_id=request.POST.get("user_id"),
            product_id=request.POST.get("product_id")
            )
        if query:
            query[0].product_count = query[0].product_count+int(request.POST.get("product_count"))
            query[0].save()
            return Response(status=status.HTTP_200_OK)

    def get(self, request, pk, *args, **kwargs):
        return self.list(request, pk, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if models.UserCart.objects.filter(
            user_id=request.POST.get("user_id"),
            product_id=request.POST.get("product_id")
            ).exists():
            return self.update(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class CreateOrderView(generics.GenericAPIView,mixins.ListModelMixin, 
    mixins.CreateModelMixin,):
    permission_classes = [IsAuthenticated]
    queryset = models.OrderDetailsModel.objects.all()
    serializer_class = serializers.CreateOrderSerializer

    def get_queryset(self, pk):
        queryset = models.OrderDetailsModel.objects.filter(user_id=pk).values(
            'product_id__p_name', 'product_id__p_desc', 'product_id__p_category__c_name', 'product_id__p_brand__b_name'
        )
        return queryset
    
    
    def list(self, request, pk=None, *args, **kwargs):
        if pk:
            queryset = models.OrderDetailsModel.objects.filter(user_id=pk)
        else:
            queryset = models.OrderDetailsModel.objects.all().order_by('-date_time')

        product_lst = []
        for query in queryset:
            product_details = models.ProductModel.objects.filter(id=query.product_id.id).first()
            serializer = serializers.ProductSerializer(product_details)
            context={
                'name':f"{query.ft_name} {query.lt_name}",
                'address':f"{query.address} {query.zip} {query.phone}",
                'product_count':query.product_count,
                'product_name':product_details.p_name,
                'product_img':serializer.data['p_img'],
                'product_price':product_details.p_price,
                'date_time':query.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            product_lst.append(context)
        response = {'product_lst':product_lst}
        return Response(response)

    def get(self, request, pk=None, *args, **kwargs):
        return self.list(request, pk, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RemoveItemFromCart(generics.GenericAPIView):
    def get(self, request, pk, *args, **kwargs):
        models.UserCart.objects.filter(user_id=pk).delete()
        return Response(status=status.HTTP_200_OK)


class UserListView(generics.GenericAPIView,mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get(self, request,*args, **kwargs):
        user_lst = models.User.objects.all()
        user_list_data=[]
        for user in user_lst:
            products = models.ProductModel.objects.filter(orderdetailsmodel__user_id=user.id).count()
            contect={
                'id':user.id,
                'name':user.username,
                'is_staff':user.is_staff,
                'is_active':user.is_active,
                'product_cnt':products
            }
            user_list_data.append(contect)
        return Response({'user_lst':user_list_data})

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        user_obj = models.User.objects.filter(id=user_id).first()
        user_obj.is_active = not user_obj.is_active
        user_obj.save()
        return Response(status=status.HTTP_200_OK)
    
from django.db.models import Sum
class BestSellerView(generics.GenericAPIView,mixins.ListModelMixin):
    def get(self, request,*args, **kwargs):
        top_products = models.ProductModel.objects.annotate(
            total_count=Sum('orderdetailsmodel__product_count')
            ).order_by('-total_count')[:8]
        serialized_data = serializers.ProductSerializer(top_products, many=True)
        return Response(serialized_data.data)


class SearchFilter(generics.GenericAPIView,mixins.ListModelMixin):
    def post(self, request,*args, **kwargs):
        search_text = request.POST.get("search_text")
        names = search_text.split() 
        if len(names) == 0:
            products= models.ProductModel.objects.all()
        elif len(names) == 1:
            products = models.ProductModel.objects.filter(p_name__contains=names[0]) 
        else:
            product_lst = []
            for ele in names:
                products = models.ProductModel.objects.filter(p_name__contains=ele) 
                product_lst.extend(products)
            products = product_lst
        serialized_data = serializers.ProductSerializer(products, many=True)
        return Response(serialized_data.data)