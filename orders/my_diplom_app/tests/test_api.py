from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
import json

from my_diplom_app.models import Product, User, Order, OrderItem, ProductInfo
from my_diplom_app.serializers import ProductSerializer, OrderItemsSerializer, OrderSerializer, ProductInfoSerializer
# class UserApiTestCase(APITestCase):
#     def register_user_test(self):
#         url = reverse('')



class GoodsApiTestCase(APITestCase):

    def test_create_user_max(self):
        url = 'http://127.0.0.1:8000/auth/users/'
        data = {
            'username': 'test_user_1',
            'password': 'Netology',
            'email': 'ilgizahiyarov95@gmail.com',
            'first_name': 'Simpson',
            'last_name': 'Gamer',
            'company': 'sitilink',
            'position': 'markrting',
            'type': 'seller',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)   
        self.assertEqual(1, User.objects.count()) 
        self.assertEqual('test_user_1', User.objects.all().last().username)
        self.assertEqual('seller', User.objects.all().last().type)


    def test_create_user_min(self):
        url = 'http://127.0.0.1:8000/auth/users/'
        data = {
            'username': 'test_user_2',
            'password': 'Netology',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)   
        self.assertEqual(1, User.objects.count()) 
        self.assertEqual('test_user_2', User.objects.all().last().username)
        self.assertEqual('buyer', User.objects.all().last().type)


    def test_bad_registration_data_no_username(self):
        url = 'http://127.0.0.1:8000/auth/users/'
        data = {
            'username': '',
            'password': 'Netology',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)   
        self.assertEqual('This field may not be blank.', response.data['username'][0])
        self.assertEqual(0, User.objects.count()) 


    def test_bad_registration_data_no_password(self):
        url = 'http://127.0.0.1:8000/auth/users/'
        data = {
            'username': 'test_user_1',
            'password': '',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)   
        self.assertEqual('This field may not be blank.', response.data['password'][0])
        self.assertEqual(0, User.objects.count()) 


    def test_bad_registration_data_short_password(self):
        url = 'http://127.0.0.1:8000/auth/users/'
        data = {
            'username': 'test_user_1',
            'password': '1q',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)   
        self.assertEqual('This password is too short. It must contain at least 8 characters.', response.data['password'][0])
        self.assertEqual(0, User.objects.count()) 


    def test_bad_registration_data_common_password(self):
        url = 'http://127.0.0.1:8000/auth/users/'
        data = {
            'username': 'test_user_1',
            'password': 'qwerty1234',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)   
        self.assertEqual('This password is too common.', response.data['password'][0])
        self.assertEqual(0, User.objects.count()) 
    

    def test_bad_registration_data_entirely_numeric_password(self):
        url = 'http://127.0.0.1:8000/auth/users/'
        data = {
            'username': 'test_user_1',
            'password': '7348973498934',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)   
        self.assertEqual('This password is entirely numeric.', response.data['password'][0])
        self.assertEqual(0, User.objects.count()) 


    def test_bad_registration_data_duplicate_login(self):
        self.test_create_user_max()
        url = 'http://127.0.0.1:8000/auth/users/'
        data = {
            'username': 'test_user_1',
            'password': 'Netology',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)   
        self.assertEqual('A user with that username already exists.', response.data['username'][0])
        self.assertEqual(1, User.objects.count()) 

#############   login  #######################

    def test_login(self):
        self.test_create_user_max()
        url = 'http://127.0.0.1:8000/auth/token/login/'
        data = {
            'username': 'test_user_1',
            'password': 'Netology',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.my_token = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('auth_token', ''.join(response.data.keys()))


    def test_login_buyer(self):
        self.test_create_user_min()
        url = 'http://127.0.0.1:8000/auth/token/login/'
        data = {
            'username': 'test_user_2',
            'password': 'Netology',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.my_token = response.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('auth_token', ''.join(response.data.keys()))


    def test_bad_login_username(self):
        self.test_create_user_max()
        url = 'http://127.0.0.1:8000/auth/token/login/'
        data = {
            'username': 'No_user',
            'password': 'Netology',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.my_token = response.data
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Unable to log in with provided credentials.', response.data['non_field_errors'][0])
     

    def test_bad_login_password(self):
        self.test_create_user_max()
        url = 'http://127.0.0.1:8000/auth/token/login/'
        data = {
            'username': 'test_user_1',
            'password': 'BadPassword',
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.my_token = response.data
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Unable to log in with provided credentials.', response.data['non_field_errors'][0])
     

    ######### logout ###########

    def test_logout(self):
        self.test_login()
        url = 'http://127.0.0.1:8000/auth/token/logout/'
        headers = {'Authorization': 'Token '+self.my_token['auth_token']}     
        response = self.client.post(url, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        
    ######### Update Product #########

    def test_update_goods_seller_user(self):
        self.test_login()
        url = 'http://127.0.0.1:8000/api/v1/update/'
        headers = {'Authorization': 'Token '+self.my_token['auth_token']}     
        response = self.client.post(url, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(0, Product.objects.count())


    def test_bad_update_goods_no_authorization(self):
        self.test_login()
        url = 'http://127.0.0.1:8000/api/v1/update/'
        # headers = {'Authorization': 'Token '+self.my_token['auth_token']}     
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual('Authentication credentials were not provided.', response.data['detail'])
     
        
    def test_bad_update_goods_invalid_token(self):
        self.test_login()
        url = 'http://127.0.0.1:8000/api/v1/update/'
        headers = {'Authorization': 'Token by_8734874834834'}     
        response = self.client.post(url, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual('Invalid token.', response.data['detail'])
    

    def test_update_goods_buyer_user(self):
        self.test_login_buyer()
        url = 'http://127.0.0.1:8000/api/v1/update/'
        headers = {'Authorization': 'Token '+self.my_token['auth_token']}     
        response = self.client.post(url, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('insufficient rights', response.data['description'])

    ######### Get Product #########

    def test_get_goods(self):
        self.test_update_goods_seller_user()
        url = reverse('goods') 
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer_data = ProductSerializer(Product.objects.all(), many=True).data
        self.assertEqual(serializer_data, response.data)



    def test_get_good(self):
        self.test_update_goods_seller_user()
        url = 'http://127.0.0.1:8000/api/v1/product/3'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)



    ######### Orders #########



    def test_post_orders(self):
        self.test_update_goods_seller_user()
        quaryset = Product.objects.all()
        serializer = ProductSerializer(quaryset, many=True)
        product_id = serializer.data[0]['id']
        shop_id = serializer.data[0]['category']['shops'][0]['id']

        url = 'http://127.0.0.1:8000/api/v1/my_basket/'
        headers = {'Authorization': 'Token '+self.my_token['auth_token']}  
        data = {
            'product': product_id,
            'shop': shop_id,
            'quantity': 1
        }
        json_data = json.dumps(data)  
        response = self.client.post(url, data=json_data, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(True, response.data['status'])
        self.assertEqual(1, OrderItem.objects.count())
        quareset = OrderItem.objects.all()
        serializer = OrderItemsSerializer(quareset, many=True)
        self.assertEqual(1, serializer.data[0]['quantity'])

        # Change

        data = {
            'product': product_id,
            'shop': shop_id,
            'quantity': 3
        }
        json_data = json.dumps(data)  
        response = self.client.post(url, data=json_data, content_type='application/json', headers=headers)
        quareset = OrderItem.objects.all()
        serializer = OrderItemsSerializer(quareset, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, serializer.data[0]['quantity'])
        

        # get

        response = self.client.get(url, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer_data = OrderSerializer(Order.objects.all(), many=True).data
        self.assertEqual(serializer_data, response.data)



        # del bad id

        quaryset = OrderItem.objects.all()
        serializer = OrderItemsSerializer(quaryset, many=True)
        order_id = serializer.data[0]['id']
        data = {
            'id': 23,  
        }
        json_data = json.dumps(data)  
        response = self.client.delete(url, data=json_data, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(False, response.data['status'])
        self.assertEqual('id not found', response.data['description'])
        self.assertEqual(1, OrderItem.objects.count())

       #  del

        quaryset = OrderItem.objects.all()
        serializer = OrderItemsSerializer(quaryset, many=True)
        order_id = serializer.data[0]['id']
        data = {
            'id': order_id,  
        }
        json_data = json.dumps(data)  
        response = self.client.delete(url, data=json_data, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(True, response.data['status'])
        self.assertEqual(0, OrderItem.objects.count())



    def orders(self):
        self.test_update_goods_seller_user()
        quaryset = Product.objects.all()
        serializer = ProductSerializer(quaryset, many=True)
        product_id = serializer.data[0]['id']
        shop_id = serializer.data[0]['category']['shops'][0]['id']
        url = 'http://127.0.0.1:8000/api/v1/my_basket/'
        headers = {'Authorization': 'Token '+self.my_token['auth_token']}   
        data = {
            'product': product_id,
            'shop': shop_id,
            'quantity': 1
        }
        json_data = json.dumps(data)  
        response = self.client.post(url, data=json_data, content_type='application/json', headers=headers)
       



 ########## confirmation ###########
    
    def test_confirmation(self):
        self.orders()
        url = 'http://127.0.0.1:8000/api/v1/confirmation/'
        headers = {'Authorization': 'Token '+self.my_token['auth_token']}   
        data = {
            'type': 'phone',
            'value': '',
        }
        json_data = json.dumps(data)  
        response = self.client.post(url, data=json_data, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(False, response.data['status'])
        self.assertEqual('not all parameters were passed', response.data['description'])



        data = {
            'type': 'phone',
            'value': '45345435',
        }
        json_data = json.dumps(data)  
        response = self.client.post(url, data=json_data, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('specify', response.data['status'])
   
        data = {
            'type': 'address',
            'value': 'Springfield',
        }
        json_data = json.dumps(data)  
        response = self.client.post(url, data=json_data, content_type='application/json', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(True, response.data['status'])
   
