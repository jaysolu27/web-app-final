import json
from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.models import Session
from django.shortcuts import redirect, render
from django.views import View
from userApp import apiCalls
from rest_framework import status
from userApp import constants
from django.utils.decorators import method_decorator

# Create your views here.
def is_loggedIn(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('user'):
            return func(request, *args, **kwargs)
        else:
            return redirect('login_page')
    return wrapper



class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="user_login.html", context={})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password_id")
        reqData = {'username':username, 'password':password}
        res = apiCalls.login_api(reqData)
        if res.status_code == status.HTTP_200_OK:
            request.session['refresh_token'] = res.json().get("refresh")
            request.session['access_token'] = res.json().get("access")
            request.session['user'] = {
                "refresh_token":res.json().get("refresh"),
                "access_token":res.json().get("access"),
                "refresh_token":res.json().get("refresh"),
                "is_staff":res.json().get("is_staff"),
                "id":res.json().get("id"),
                "username":res.json().get("username"),

            }
            if res.json().get("is_staff"):
                return redirect('brand_name')
            else:
                return redirect('home_page')
        
        
        return render(request, template_name="user_login.html", context={'message':'please enter valid credentials'})
    

class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name="user_register.html", context={})

    def post(self, request, *args, **kwargs):
        req_data = {}
        req_data["username"] = request.POST.get("username")
        req_data["name"] = request.POST.get("name")
        req_data["email"] = request.POST.get("email")
        req_data["password"] = request.POST.get("password")
        req_data["checkpassword"] = request.POST.get("checkpassword")

        res = apiCalls.register_api(req_data)
        if res.status_code == status.HTTP_201_CREATED:
            return redirect('login_page')
        return render(request, template_name="user_register.html", context={})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect('login_page')

@method_decorator(is_loggedIn, name='dispatch')
class HomePageView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        res= apiCalls.fetch_top_products(
            token=self.request.session.get('user').get("access_token")
        )
        return render(request, template_name="home.html", 
                      context={
                        "product_lst":res.json(), 
                        'user_name':request.session.get("user").get("username")
                        })

    def post(self):
        pass


@method_decorator(is_loggedIn, name='dispatch')
class ShopPageView(View):

    def get_api_request_context(self):
        context={}
        for item in constants.FILTER_FIELDS.__members__.values():
            if self.request.session.get(item.value):
                context[item.value] = self.request.session.get(item.value)
        return context
    

    def create_context(self, context, product_api_call, category_api_call, brand_api_call, filter_type=False):
        if filter_type:
            request_data = self.get_api_request_context()
            product_lst = product_api_call(request_data,token=self.request.session.get('user').get("access_token"))
        else:
            product_lst = product_api_call(token=self.request.session.get('user').get("access_token"))
        category_lst = category_api_call(token=self.request.session.get('user').get("access_token"))
        brand_lst = brand_api_call(token=self.request.session.get('user').get("access_token"))

        if category_lst.status_code == status.HTTP_403_FORBIDDEN:
            return None
        if brand_lst.status_code == status.HTTP_403_FORBIDDEN:
            return None
        if product_lst.status_code == status.HTTP_403_FORBIDDEN:
            return None
        
        context["category_lst"] = (
            category_lst.json()
            if category_lst.status_code == status.HTTP_200_OK
            else None
        )
        context["brand_lst"] = (
            brand_lst.json()
            if brand_lst.status_code == status.HTTP_200_OK
            else None
        )
        context["product_lst"] = (
            product_lst.json()
            if brand_lst.status_code == status.HTTP_200_OK
            else None
        )
        return context
    
    def filter_func(self, request):
        context = {
            "key": request.GET.get('key'),
            "val_1":request.GET.get('val'),
        }

        if request.session.get(context["key"]) == context["val_1"]:
            del request.session[context["key"]]
            if context["key"] == "p_category__id" and request.session.get(f'cat_{context["key"]}'):
                del request.session[f'cat_{context["key"]}']
            if context["key"] == "p_brand__id" and request.session.get(f'brand_{context["key"]}'):
                del request.session[f'brand_{context["key"]}']
            if context["key"] == "p_price" and request.session.get(f'price_{context["key"]}'):
                del request.session[f'price_{context["key"]}']

        else:
            request.session[context["key"]] = context["val_1"]
            if context["key"] == "p_category__id":
                request.session[f'cat_{context["key"]}'] = request.GET.get('val')
            if context["key"] == "p_brand__id":
                request.session[f'brand_{context["key"]}'] = request.GET.get('val')
            if context["key"] == "price":
                request.session[f'price_{context["key"]}'] = request.GET.get('val')
            
        # api_request 
        res_data=self.create_context(
            context, 
            apiCalls.fetch_filter_product_api,
            apiCalls.fetch_all_category_api,
            apiCalls.fetch_all_brands_api,
            filter_type=True
            )

        context['cat_p_category__id']=request.session.get(f'cat_p_category__id')
        context['brand_p_brand__id']=request.session.get(f'brand_p_brand__id')
        context['price_price']=request.session.get(f'price_price')

        if res_data == None:
            return redirect("logout_page")
        return res_data
    

    def get(self, request, *args, **kwargs): 
        
        if request.GET.get('key'):
            request.session[f"{request.GET.get('key')}_val"]=request.GET.get('val')
            res_data = self.filter_func(request)
            return render(request, template_name="shop.html", context=res_data)
        else:
            if request.session.get("p_brand__id"):
                del request.session["p_brand__id"]
            if request.session.get("p_category__id"):
                del request.session["p_category__id"]
            if request.session.get("p_price"):
                del request.session["p_price"]
            if request.session.get(f'cat_p_category__id'):
                del request.session['cat_p_category__id']
            if request.session.get(f'brand_p_brand__id'):
                del request.session['brand_p_brand__id']
            context = {
                "brand_id": None,
                "category_id":None,
                "product_lst": None,
            } 
            context=self.create_context(
                context, 
                apiCalls.fetch_products_api,
                apiCalls.fetch_all_category_api,
                apiCalls.fetch_all_brands_api
                )
            if context == None:
                return redirect("logout_page")
            
            context['product_cnt'] = len(context['product_lst'])
            context['user_name']=request.session.get("user").get("username")
            return render(request, template_name="shop.html", context=context)


    def post(self, request, *args, **kwargs):
        search_text = request.POST.get('search_text')
        context = {
                "brand_id": None,
                "category_id":None,
                "product_lst": None
            } 
        
        context=self.create_context(
            context, 
            apiCalls.fetch_products_api,
            apiCalls.fetch_all_category_api,
            apiCalls.fetch_all_brands_api
            )
        if context == None:
            return redirect("logout_page")
        res = apiCalls.search_products_api(
            {'search_text':search_text},
            token=self.request.session.get('user').get("access_token")
        )
        context["product_lst"] = res.json()
        context['product_cnt'] = len(context['product_lst'])
        context['user_name']=request.session.get("user").get("username")
        return render(request, template_name="shop.html", context=context)


@method_decorator(is_loggedIn, name='dispatch')
class ProductDetailView(View):
    def get(self, request, pk=None, *args, **kwargs):
        res = apiCalls.fetch_product_detail_api(pk, token=self.request.session.get('user').get("access_token"))
        related_products = apiCalls.fetch_filter_product_api(
            {constants.FILTER_FIELDS.CATEGORY.value:res.json().get("p_category")},
            token=self.request.session.get('user').get("access_token")
            )
        if related_products.status_code == status.HTTP_403_FORBIDDEN:
            return redirect("logout_page")
        
        review_lst = apiCalls.fetch_all_reviews_api(
            user_id = self.request.session.get('user').get('id'),
            product_id = pk,
            token=self.request.session.get('user').get("access_token")
        )
        
        context = {
            "product_details":res.json(), 
            'related_products':related_products.json(),
            'review_lst':review_lst.json().get("review_lst"),
            }
        context['user_name']=request.session.get("user").get("username")
        return render(request, template_name="detail.html", context=context)
    
    def post(self, request, pk=None, *args, **kwargs):
        review_data = request.POST.get("review")
        product_id = request.POST.get("product_id")

        req_data={
            "user_id":self.request.session.get('user').get("id"),
            "product_id":product_id,
            "review":review_data
        }
        res = apiCalls.create_review_api(
            req_data,
            token=self.request.session.get('user').get("access_token")
        )
        return redirect("product_detail", pk=product_id)

@method_decorator(is_loggedIn, name='dispatch')
class AddToCartView(View):
    def post(self, request, pk=None, *args, **kwargs):
        req_data = {
            "product_id": request.POST.get("product_id"),
            "product_count": request.POST.get("product_count"),
            "user_id":request.session.get('user').get("id")
        }
        response = apiCalls.add_to_cart_api(
            req_data,
            token=self.request.session.get('user').get("access_token")
            )

        if response.status_code == status.HTTP_201_CREATED or response.status_code == status.HTTP_200_OK:
            context = {"message":"Product added to cart successfully", "status":response.status_code}
            return JsonResponse(context)
        if response.status_code == status.HTTP_403_FORBIDDEN:
            return redirect("logout_page")
        if response.status_code != status.HTTP_200_OK:
            context = {"message":"Something went wrong", "status":response.status_code}
            context['user_name']=request.session.get("user").get("username")
            return JsonResponse(context)
        
    
@method_decorator(is_loggedIn, name='dispatch')
class CartView(View):
    def get(self, request, *args, **kwargs):
        res= apiCalls.fetch_cart_product_api(
            request.session.get('user').get("id"),
            token=self.request.session.get('user').get("access_token")
        )
        if res.status_code == status.HTTP_403_FORBIDDEN:
            return redirect("logout_page")
        
        context = res.json()
        return render(
            request, 
            template_name="cart.html", 
            context={
            "cart":context['data'], 
            'total_cnt':context['total_cnt'],
            'total_cost':context['total_cost'],
            'user_name':request.session.get("user").get("username")
            }
        )


    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'delete':
            tt="tt"
            res = apiCalls.delete_cart_item_api(
                request.POST.get('cart_id'),
                token=self.request.session.get('user').get("access_token")
                )
            if res.status_code == status.HTTP_401_UNAUTHORIZED or res.status_code==status.HTTP_403_FORBIDDEN:
                return redirect("logout_page")
            return redirect("cart_view")
        return render(request, template_name="cart.html")


@method_decorator(is_loggedIn, name='dispatch')
class BilingVIew(View):
    def get(self, request, *args, **kwargs):
        res= apiCalls.fetch_cart_product_api(
            request.session.get('user').get("id"),
            token=self.request.session.get('user').get("access_token")
        )
        context = res.json()
        
        return render(
            request, 
            template_name="biling.html", 
            context={
            "cart":context['data'], 
            'total_cnt':context['total_cnt'],
            'total_cost':context['total_cost'],
            'user_name':request.session.get("user").get("username"),
            'card_len':False
            }
        )

    def post(self, request, *args, **kwargs):
        card_validate = request.POST.get("card_validate")
        if len(card_validate) != 16:
            res= apiCalls.fetch_cart_product_api(
            request.session.get('user').get("id"),
            token=self.request.session.get('user').get("access_token")
            )
            context = res.json()
            return render(
                request, 
                template_name="biling.html", 
                context={
                "cart":context['data'], 
                'total_cnt':context['total_cnt'],
                'total_cost':context['total_cost'],
                'user_name':request.session.get("user").get("username"),
                'card_len':True
                }
            )
        ft_address = request.POST.get("ft_address")
        sc_address = request.POST.get("sc_address")
        address = f"{ft_address} {sc_address}"
        res= apiCalls.fetch_cart_product_api(
            request.session.get('user').get("id"),
            token=self.request.session.get('user').get("access_token")
        )
        response = res.json().get('data')
        order_lst = []
        for item in response:
            context ={
                    "ft_name":request.POST.get("ft_name"),
                    "lt_name" : request.POST.get("lt_name"),
                    "country" : request.POST.get("country_name"),
                    "address":address,
                    "town":request.POST.get("town"),
                    "state":request.POST.get("state"),
                    "zip":request.POST.get("zip"),
                    "phone":request.POST.get("phone"),
                    "email":request.POST.get("email"),
                    "user_id":request.session.get('user').get("id"),
                    "product_id":item["product_id"],
                    "product_count":item["count"],
                    }
            order_lst.append(context)
        for itm in order_lst:
            res= apiCalls.create_order_api(
                itm,
                token=self.request.session.get('user').get("access_token")
            )
        res=apiCalls.delete_cart(
            request.session.get('user').get("id"),
            token=self.request.session.get('user').get("access_token")
            )
        return redirect('my_orders_success', success="True")



@method_decorator(is_loggedIn, name='dispatch')
class OrderHistoryView(View):
    def get(self, request, success=False, *args, **kwargs):
        res= apiCalls.list_order_api(
            request.session.get('user').get("id"),
            token=self.request.session.get('user').get("access_token")
        )
        if success:
            success = True
        res_data = res.json()
        return render(
            request, 
            template_name="order_history.html", 
            context={
            "order_lst":res_data['product_lst'],
            'user_name': request.session.get("user").get("username"),
            "success":success
            }
        )


@method_decorator(is_loggedIn, name='dispatch')
class AboutUsView(View):
    def get(self, request, success=False, *args, **kwargs):
        return render(
            request, 
            template_name="aboutus.html", 
            context={
            'user_name': request.session.get("user").get("username"),
            }
        )


@method_decorator(is_loggedIn, name='dispatch')
class ContactUsView(View):
    def get(self, request, success=False, *args, **kwargs):
        return render(
            request, 
            template_name="contactus.html", 
            context={
            'user_name': request.session.get("user").get("username"),
            }
        )