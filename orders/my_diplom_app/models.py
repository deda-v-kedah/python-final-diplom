from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    filename = models.CharField(max_length=50)

    class Meta:
        unique_together = ['name',]



class Category(models.Model):
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories', blank=True)
    name = models.CharField(max_length=40, verbose_name='Название')


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', blank=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=80, verbose_name='Название')


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='product_infos', blank=True,
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='product_infos', blank=True,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')


class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')


    class Meta:
        unique_together = ['name',]

    def __str__(self):
        return self.name



class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте',
                                     related_name='product_parameters', blank=True,
                                     on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters', blank=True,
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)


class User(AbstractUser):
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)
    type = models.CharField(verbose_name='Тип пользователя',  max_length=8, default='buyer')




class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус', max_length=15)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='ordered_items',
                                     blank=True,
                                     on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='ordered_items', blank=True,
                              on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')



class Contact(models.Model):
    type = models.CharField(max_length=50, verbose_name="Тип")
    user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)