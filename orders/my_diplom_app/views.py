from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist

import yaml

from my_diplom_app.models import Shop, Product, Category, ProductInfo, Parameter, ProductParameter, Order, OrderItem
from my_diplom_app.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer



class UpdateView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        if request.user.type == 'seller':

            with open('../data/shop1.yaml') as file:
                data = yaml.safe_load(file)

                shop, _ = Shop.objects.get_or_create(name=data['shop'])

                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()    
            
                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                    product_info, _ = ProductInfo.objects.get_or_create(product_id=product.id,
                                                                shop=shop,
                                                                name=item['model'],
                                                                price=item['price'],
                                                                price_rrc=item['price_rrc'],
                                                                quantity=item['quantity'],
                                                                )
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.get_or_create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)


            return JsonResponse({'Status': True, 'Code': 201})
        else:
            return JsonResponse({'Status': False, 'error': 403, 'описание:': 'недостаточно прав'})
     



class GoodsView(APIView):
    def get(self, request, *args, **kwargs):

        quaryset = Product.objects.all()
        serializer = ProductSerializer(quaryset, many=True)

        return Response(serializer.data)

   

class ProductView(APIView):
    def get(self, request, id, *args, **kwargs):

        quareset = Product.objects.filter(id=id)
        serializer = ProductSerializer(quareset, many=True)

        return Response(serializer.data)
    

class BasketView(APIView):

    def get(self, request, *args, **qwargs):

        quareset = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(quareset, many=True)

        return Response(serializer.data)


    def post(self, request, *args, **qwargs):
        
        if 'product' in request.data and 'shop' in request.data and 'quantity' in request.data:
            

            try:

                product = Product.objects.get(id=request.data['product'])
                shop = Shop.objects.get(id=request.data['shop'])
                info = ProductInfo.objects.get(product_id = request.data['product'])


                if (info.quantity >= int(request.data['quantity'])):

                    order, _ = Order.objects.get_or_create(user_id=request.user.id, status='not_confirmed')
                
                    OrderItem.objects.filter(order=order, product=product, shop=shop).update(quantity=request.data['quantity'])

                    order_item, _ = OrderItem.objects.get_or_create(order=order, product=product, shop=shop, quantity=request.data['quantity'])


                    return Response({'Status': True, 'Code': 201, 'id': order_item.id})
                

                else:
                    return Response({'Status': False, 'Error': 400, 'описание': 'Количество товаров в карзине выше, чем имеется'})
                
            except Shop.DoesNotExist:
                return Response({'Status': False, 'Error': 400, 'описание': 'Скорее всего не верный id магазинa'})
            except Product.DoesNotExist:
                return Response({'Status': False, 'Error': 400, 'описание': 'Скорее всего не верный id товара'})
                
        
        
        
        
        else:
            return Response({'Status': False, 'Error': 400, 'описание': 'Переданы не все параметры'})
            

        
    def delete(self, request, *args, **kwargs):
        if 'id' in request.data:
            OrderItem.objects.filter(id=request.data['id']).delete()
            return Response({'Status': True, 'Code': 410, 'описание': 'успешно удалено'})
        else:
            return Response({'Status': False, 'Code': 400, 'описание': 'Переданы не все параметры'})

            



    
