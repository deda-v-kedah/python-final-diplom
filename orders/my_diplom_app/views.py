from django.shortcuts import render
from django.db import IntegrityError

from rest_framework.response import Response
from rest_framework.views import APIView

import yaml

from my_diplom_app.models import Shop, Product, Category, ProductInfo, Parameter, ProductParameter
from my_diplom_app.serializers import ProductSerializer


class UpdateView(APIView):
    def get(self, request, *args, **kwargs):

        with open('../data/shop1.yaml') as file:
            docs = yaml.safe_load_all(file)


            for doc in docs:
                for key, val in doc.items():
                    if type(val) == list:
                        for i in val:
                            if key == 'categories':
                                category = Category.objects.create( id = i['id'], name = i['name'])
                                category.shops.add(shop.id)
                            if key == 'goods':
                                product = Product.objects.create(id = i['id'],
                                                                name = i['model'],
                                                                category = Category.objects.get(id=i['category']),
                                                                )
                                
                                product_info = ProductInfo.objects.create(product = product,
                                                shop = shop,
                                                name = i['name'],
                                                price = i['price'],
                                                price_rrc = i['price_rrc'],
                                                quantity = i['quantity'],
                                                )

                                
                                for key_param, val_param in i['parameters'].items():
                                    try:
                                        parameter = Parameter.objects.create(name = key_param)

                                        
                                    except(IntegrityError):
                                        print('this parameter is available in the database')

                                    product_parameter = ProductParameter.objects.create(
                                                        product_info=product_info,
                                                        parameter=Parameter.objects.get(name=key_param),
                                                        value=val_param
                                                        )


                                       



                    else:
                        shop = Shop.objects.create(name = val)

           


     

        
        quaryset = Product.objects.all()
        serializer = ProductSerializer(quaryset, many=True)
        return Response(serializer.data)