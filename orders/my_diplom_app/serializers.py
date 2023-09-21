from rest_framework import serializers
from rest_framework.settings import api_settings
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction


from djoser.conf import settings
from djoser.compat import get_user_email, get_user_email_field_name


from my_diplom_app.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact, User






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "company",
            "position",
            "type",
            "last_login",
            "date_joined",


        )
        
        read_only_fields = (settings.LOGIN_FIELD,)

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        instance.email_changed = False
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.email_changed = True
                instance.save(update_fields=["is_active"])
        return super().update(instance, validated_data)




class UserCreateMixin:
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


class UserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
            "first_name",
            "last_name",
            "company",
            "position",
            "type",
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs










class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name',  )


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()
    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value')


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'creater_email')




class CategorySerializer(serializers.ModelSerializer):
    shops = ShopSerializer(many=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'shops')


class ProductInfoSerializer(serializers.ModelSerializer):
    product_parameters = ProductParameterSerializer(many=True)
    class Meta:
        model = ProductInfo
        fields = ('quantity', 'price', 'price_rrc', 'product_parameters')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_infos = ProductInfoSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id',  'name', 'product_infos', 'category')






class ConfirmProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ('quantity', 'price', 'price_rrc')



class ConfirmProductSerializer(serializers.ModelSerializer):
    product_infos = ConfirmProductInfoSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id',  'name', 'product_infos',)



class OrderItemsSerializer(serializers.ModelSerializer):
    product = ConfirmProductSerializer()
    shop = ShopSerializer()
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'shop', 'quantity', )


class OrderSerializer(serializers.ModelSerializer):
    ordered_items =  OrderItemsSerializer(many=True)
    class Meta:
        model = Order
        fields = ('id', 'user_id', 'dt', 'status', 'ordered_items')





class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'type', 'user', 'value', )

