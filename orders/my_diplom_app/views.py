from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist

import yaml
import requests
import json

from my_diplom_app.models import Shop, Product, Category, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact
from my_diplom_app.serializers import CategorySerializer, ProductSerializer, OrderSerializer

from my_diplom_app.tasks import send



def auth(request):
    return render(request, 'oauth.html')


class ConfirmationView(APIView):
    """Confirmation of an order"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if 'value' in request.data and request.data['value'] != '':

            quaryset = Order.objects.get(user_id = request.user.id)
            serializer = OrderSerializer(quaryset)

            list_shops = []
            text = ''
            text_dict = {}

            for i in serializer.data['ordered_items']:
                if not i['shop']['id'] in text_dict.keys():
                    text = f"Здравствуйте, {i['shop']['creater_email']} в вашем магазине {i['shop']['name']} был осуществлен заказ:\n\n\n"
               
                list_shops.append(i['shop']['creater_email'])

                text += f"наименование: {i['product']['name']}\n"
                text += f"инв. №(id): {i['product']['id']}\n"
                text += f"стоимость еденицы: {i['product']['product_infos'][0]['price_rrc']}\n"
                text += f"количество: {i['quantity']} шт\n\n"
            
                text_dict[i['shop']['id']] = text



                unique_shops = list(set(list_shops))



            if 'type' in request.data and request.data['type'] == 'phone':
                contact, _ = Contact.objects.get_or_create(user_id=request.user.id, type=request.data['type'], value=request.data['value'])
                for k,v in text_dict.items():
                    send.delay('Позвонить', f'позвонить для уточнения адресса по номеру {request.data["value"]}, детали заказа {serializer.data}', unique_shops)              
                send.delay('Ваш заказ в стадии уточнение', f'Вы не укозали аддрес наш оператор свяжется с вами по номеру {request.data["value"]}', [request.user.email])
                return Response({'status': 'specify',
                                 'num': request.data["value"],
                                 'data': serializer.data})
            elif 'type' in request.data and request.data['type'] == 'address':
                contact, _ = Contact.objects.get_or_create(user_id=request.user.id, value=request.data['value'])
                for k,v in text_dict.items():
                    send.delay('Накладная', text_dict[k], unique_shops)
                send.delay('Ваш заказ одробен', 'Ваш заказ одробен бла бла бла', [request.user.email])
                return Response({'status': True,
                                 'data': serializer.data})
            else:
                return Response({'status': False,
                                 'data':'number or address required'})
        else:
            return Response({'status': False,  'description': 'not all parameters were passed'})
 


class UpdateView(APIView):
    """Update products"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        if request.user.type == 'seller':


            with open('../data/shop1.yaml') as file:
                data = yaml.safe_load(file)

                shop, _ = Shop.objects.get_or_create(name=data['shop'], creater_email=request.user.email)

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


            return Response({'status': True})
        else:
            return Response({'status': False,
                             'description': 'insufficient rights'})
     



class GoodsView(APIView):
    """Product withdrawal"""
    def get(self, request, *args, **kwargs):

        quaryset = Product.objects.all()
        serializer = ProductSerializer(quaryset, many=True)

        return Response(serializer.data)

   

class ProductView(APIView):
    """Card Product"""
    def get(self, request, id, *args, **kwargs):

        quareset = Product.objects.filter(id=id)
        serializer = ProductSerializer(quareset, many=True)

        return Response(serializer.data)
    

class BasketView(APIView):
    """Cart of goods"""
    permission_classes = [permissions.IsAuthenticated]

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


                    return Response({'status': True, 'id': order_item.id})
                

                else:
                    return Response({'status': False, 'description': 'The number of items in the cart is higher than available'})
            
            


            except Shop.DoesNotExist:
                return Response({'status': False,  'description': 'Most likely the store ID is not correct'})
            except Product.DoesNotExist:
                return Response({'status': False,  'description': 'Most likely the product ID is incorrect'})
                
        
        else:
            return Response({'status': False,  'description': 'Not all parameters were passed'})
            

        
    def delete(self, request, *args, **kwargs):
        if 'id' in request.data:
            if OrderItem.objects.filter(id=request.data['id']).exists():
                OrderItem.objects.filter(id=request.data['id']).delete()
                return Response({'status': True, })
            else:
                return Response({'status': False,  'description': 'id not found'})
            
        else:
            return Response({'status': False,  'description': 'not all parameters were passed'})

            



    
