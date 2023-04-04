from rest_framework import serializers
from .models import OrderDetailsModel, ProductModel, CategoryModel, BrandModel, ReviewModel, UserCart
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator



class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'password']
        # write_only_fields = ['password']
    
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name


class getJWTTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except Exception as e:
            print(e)
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["is_staff"] = self.user.is_staff
        data["id"] = self.user.id

        return data


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])   
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'token', 'password']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'
    def create(self, validated_data):
        product = ProductModel.objects.create(
            p_name=validated_data['p_name'],
            p_desc=validated_data['p_desc'],
            p_category=validated_data['p_category'],
            p_brand=validated_data['p_brand'],
            p_img=validated_data['p_img'],
            p_price=validated_data['p_price']
        )
        return product

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetailsModel
        fields = '__all__'