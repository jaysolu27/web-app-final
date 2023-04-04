from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from requests import Response
from adminApp import apicalls
from rest_framework import status
# Create your views here.
from django.utils.decorators import method_decorator

from apiApp import models, serializers

# Create your views here.
def is_staff_loggedIn(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('user') and request.session.get('user').get('is_staff'):
            return func(request, *args, **kwargs)
        else:
            return redirect('login_page')
    return wrapper

class AdminLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='login.html')


@method_decorator(is_staff_loggedIn, name='dispatch')
class DashBoardView(View):

    def get(self, request, *args, **kwargs):
        return render(request, template_name='dashboard.html', context={})

    def post(self, request, *args, **kwargs):
        form_data = request.POST
        res = apicalls.login_api(form_data)
        if res.status_code == status.HTTP_200_OK:
            print("login")
        print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        print(res.json())
        print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        return render(request, template_name='dashboard.html', context={})


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='register.html', context={})

    def post(self, request, *args, **kwargs):
        form_data = request.POST
        res = apicalls.register_api(form_data)
        if res.status_code == status.HTTP_200_OK:
            print("register")
        print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        print(res.json())
        print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        return render(request, template_name='register.html', context={})
    

@method_decorator(is_staff_loggedIn, name='dispatch')
class BrandView(View):
    def fetch_brand_data(self):
        res = apicalls.fetch_brand_list_api(
            token=self.request.session.get('user').get("access_token")
        )
        if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
            return redirect("logout_page")
        return res.json()

    def get(self, request, *args, **kwargs):
        brand_lst = self.fetch_brand_data()
        return render(request, template_name='brand.html', context={"brand_lst":brand_lst})

    def post(self, request, *args, **kwargs):
        form_data = request.POST
        msg = "something went wrong"
        if 'form2-delete' in request.POST:
            res=apicalls.delete_brand_api(
                form_data.get('type_id'),
                token=self.request.session.get('user').get("access_token")
                )
            if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
                return redirect("logout_page")
            brand_lst = self.fetch_brand_data()
            return render(
            request, 
            template_name='brand.html', 
            context={"brand_lst":brand_lst, "status":"deleted successfully", "code":200}
            )

        else:
            if form_data.get('type_id'):
                res = apicalls.update_brand_api(form_data, form_data.get('type_id'),token=self.request.session.get('user').get("access_token"))
                if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
                    return redirect("logout_page")
            else:
                res = apicalls.create_brand_api(form_data,token=self.request.session.get('user').get("access_token"))

        if res.status_code == status.HTTP_201_CREATED or res.status_code == status.HTTP_200_OK :
            msg = res.json().get("msg")
        else:
            msg = [elem[0] for elem in res.json().values()][0]
        brand_lst = self.fetch_brand_data()
        return render(
            request, 
            template_name='brand.html', 
            context={"brand_lst":brand_lst, "status":msg, "code":res.status_code}
            )

@method_decorator(is_staff_loggedIn, name='dispatch')
class CategoryView(View):

    def fetch_category_data(self):
        res = apicalls.fetch_category_list_api(token=self.request.session.get('user').get("access_token"))
        if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
            return redirect("logout_page")
        if res.status_code != status.HTTP_200_OK:
            raise Exception
        return res.json()

    def get(self, request, *args, **kwargs):
        category_lst = self.fetch_category_data()
        return render(request, template_name='category.html', context={"category_lst":category_lst})

    def post(self, request, *args, **kwargs):
        form_data = request.POST
        msg = "something went wrong"
        if 'form2-delete' in request.POST:
            res=apicalls.delete_category_api(form_data.get('type_id'),token=self.request.session.get('user').get("access_token"))
            if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
                return redirect("logout_page")
            category_lst = self.fetch_category_data()
            return render(
            request, 
            template_name='category.html', 
            context={"category_lst":category_lst, "status":"deleted successfully", "code":200}
            )

        else:
            if form_data.get('type_id'):
                res = apicalls.update_category_api(form_data, form_data.get('type_id'),token=self.request.session.get('user').get("access_token"))
                if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
                    return redirect("logout_page")
            else:
                res = apicalls.create_category_api(form_data,token=self.request.session.get('user').get("access_token"))
                if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
                    return redirect("logout_page")

        if res.status_code == status.HTTP_201_CREATED or res.status_code == status.HTTP_200_OK :
            msg = res.json().get("msg")
        else:
            msg = [elem[0] for elem in res.json().values()][0]
        category_lst = self.fetch_category_data()

        return render(
            request, 
            template_name='category.html', 
            context={"category_lst":category_lst, "status":msg, "code":res.status_code}
            )

@method_decorator(is_staff_loggedIn, name='dispatch')
class ProductView(View):
    def fetch_category_data(self):
        res = apicalls.fetch_category_list_api(token=self.request.session.get('user').get("access_token"))
        if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
            return redirect("logout_page")
        if res.status_code != status.HTTP_200_OK:
            raise Exception
        return res.json()
    

    def fetch_brand_data(self):
        res = apicalls.fetch_brand_list_api(
            token=self.request.session.get('user').get("access_token")
        )
        if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
            return redirect("logout_page")
        return res.json()
    
    
    def fetch_product_data(self):
        res = apicalls.fetch_products_api(token=self.request.session.get('user').get("access_token"))
        if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
            return redirect("logout_page")
        if res.status_code != status.HTTP_200_OK:
            raise Exception
        return res.json()
    
    def get_render_details(self):
        res = self.fetch_product_data()
        category_lst = self.fetch_category_data()
        brand_lst = self.fetch_brand_data()
        return [res, category_lst, brand_lst]

    def get(self, request, *args, **kwargs):
        res,category_lst,brand_lst=self.get_render_details()
        return render(
            request, 
            template_name='products.html', 
            context={"product_lst":res, 'category_lst':category_lst, 'brand_lst':brand_lst}
            )

    def post(self,request, *args, **kwargs):
        form_data = request.POST

        msg = "something went wrong"
        if 'form2-delete' in request.POST:
            res=apicalls.delete_product_api(form_data.get('type_id'),token=self.request.session.get('user').get("access_token"))
            if res.status_code == status.HTTP_403_FORBIDDEN or res.status_code == status.HTTP_401_UNAUTHORIZED:
                return redirect("logout_page")
            category_lst = self.fetch_product_data()
            return redirect("product_name")

        else:

            req_data = {
                'p_name':request.POST.get("p_name"),
                "p_desc":request.POST.get("p_desc"),
                "p_price":request.POST.get("p_price"),
                "brand_id":request.POST.get("brand_id"),
                "category_id":request.POST.get("category_id"),
                "p_img":request.FILES.get("p_img"),
            }
            
            if form_data.get('type_id'):
                if form_data.get('p_name') == '' and form_data.get('p_desc')=='' and form_data.get('p_price') == '' and request.FILES.get("p_img") =='' and request.POST.get("brand_id")=='':
                    res,category_lst,brand_lst=self.get_render_details()
                    return render(
                    request, 
                    template_name='products.html', 
                    context={"product_lst":res, 'category_lst':category_lst, 'brand_lst':brand_lst, "msg":"all fields cannot be empty"}
                    )
                
                product_obj = models.ProductModel.objects.filter(id=form_data.get('type_id')).first()
                try:
                    brand_obj = models.BrandModel.objects.filter(id=request.POST.get("brand_id")).first()
                    category_obj = models.CategoryModel.objects.filter(id=request.POST.get("category_id")).first()
                except Exception as e:
                    print(e)
                
                if form_data.get('p_name'):
                    product_obj.p_name = form_data.get('p_name')
                if form_data.get('p_desc'):
                    product_obj.p_desc = form_data.get('p_desc')
                if form_data.get('p_price'):
                    product_obj.p_price = form_data.get('p_price')
                if form_data.get('brand_id'):
                    product_obj.p_brand = brand_obj
                if form_data.get('category_id'):
                    product_obj.p_brand = brand_obj

                if request.FILES.get("p_img"):
                    product_obj.p_img = request.FILES.get("p_img")
                product_obj.save()

            else:
                if form_data.get('p_name') == '' or form_data.get('p_desc')=='' or form_data.get('p_price') == '' or request.POST.get("brand_id")=='' or request.FILES.get("p_img")=='':
                    res,category_lst,brand_lst=self.get_render_details()
                    return render(
                    request, 
                    template_name='products.html', 
                    context={"product_lst":res, 'category_lst':category_lst, 'brand_lst':brand_lst, "msg":"all fields are required"}
                    )
                brand_obj = models.BrandModel.objects.filter(id=request.POST.get("brand_id")).first()
                category_obj = models.CategoryModel.objects.filter(id=request.POST.get("category_id")).first()
                try:
                    product_obj = models.ProductModel.objects.create(
                        p_name = request.POST.get("p_name"),
                        p_desc = request.POST.get("p_desc"),
                        p_price = request.POST.get("p_price"),
                        p_brand = brand_obj,
                        p_category = category_obj,
                        p_img = request.FILES.get("p_img")
                    )
                    product_obj.save()
                except Exception as e:
                    print(e)
                product_obj.save()
            return redirect("product_name")
    

@method_decorator(is_staff_loggedIn, name='dispatch')
class UserListView(View):
    def get(self,request, *args, **kwargs):
        res = apicalls.fetch_user_list_api(
            token=self.request.session.get('user').get("access_token")
        )
        return render(
            request, 
            template_name='user_lst.html', 
            context={"user_lst":res.json()['user_lst']}
            )
    
    def post(self,request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        res= apicalls.change_user_status_api(
            {'user_id':user_id},
            token=self.request.session.get('user').get("access_token")
        )
        return JsonResponse({'user_id':user_id})
        

@method_decorator(is_staff_loggedIn, name='dispatch')
class OrderListView(View):
    def get(self,request, *args, **kwargs):
        res = apicalls.fetch_order_list_api(
            token=self.request.session.get('user').get("access_token")
        )
        return render(
            request, 
            template_name='order_list.html', 
            context={"product_lst":res.json()['product_lst']}
            )
    
    def post(self,request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        res= apicalls.change_user_status_api(
            {'user_id':user_id},
            token=self.request.session.get('user').get("access_token")
        )
        return JsonResponse({'user_id':user_id})
        