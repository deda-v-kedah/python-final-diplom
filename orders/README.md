# ПЕРЕД ТЕСТИРОВАНИЕМ

## Заменить в djoser стандартные serializator на кастомные

### В файле conf.py djoser

    "SERIALIZERS": ObjDict(
        {
            "activation": "djoser.serializers.ActivationSerializer",
            "password_reset": "djoser.serializers.SendEmailResetSerializer",
            "password_reset_confirm": "djoser.serializers.PasswordResetConfirmSerializer",
            "password_reset_confirm_retype": "djoser.serializers.PasswordResetConfirmRetypeSerializer",
            "set_password": "djoser.serializers.SetPasswordSerializer",
            "set_password_retype": "djoser.serializers.SetPasswordRetypeSerializer",
            "set_username": "djoser.serializers.SetUsernameSerializer",
            "set_username_retype": "djoser.serializers.SetUsernameRetypeSerializer",
            "username_reset": "djoser.serializers.SendEmailResetSerializer",
            "username_reset_confirm": "djoser.serializers.UsernameResetConfirmSerializer",
            "username_reset_confirm_retype": "djoser.serializers.UsernameResetConfirmRetypeSerializer",
            # "user_create": "djoser.serializers.UserCreateSerializer",
            "user_create": "my_diplom_app.serializers.UserCreateSerializer",
            "user_create_password_retype": "djoser.serializers.UserCreatePasswordRetypeSerializer",
            "user_delete": "djoser.serializers.UserDeleteSerializer",
            "user": "djoser.serializers.UserSerializer",
            # "current_user": "djoser.serializers.UserSerializer",
            "current_user": "my_diplom_app.serializers.UserSerializer",
            "token": "djoser.serializers.TokenSerializer",
            "token_create": "djoser.serializers.TokenCreateSerializer",
        }




# API для закупок

## Запросы

1 **Регестрация**\
POST запрос
* url: http://127.0.0.1:8000/auth/users/
* Headers: -
* Body
  - username *
  - password *
  - email *
  - first_name
  - last_name *
  - company
  - position
  - type (seller/buyer(по умолчанию)) *

ответ: статус код

на введенный email улетит сообщение с информацией о регестрации

2 **Вход**\
POST запрос
* url: http://127.0.0.1:8000/auth/token/login/
* Headers: -
* Body
  - username *
  - password *

ответ: myToken
  

3 **Профиль**\
Get запрос
* url: http://127.0.0.1:8000/auth/users/me/
* Headers: {Authorization: Token myToken}
* Body -

ответ: json о авторезовонном юзире
  


4 **Выгрузка товаров**\
POST запрос
* url: http://127.0.0.1:8000/update/
* Headers: {Authorization: Token myToken}
* Body -

ответ: статус код
  

5 **Список товаров**\
Get запрос
* url: http://127.0.0.1:8000/goods/
* Headers: -
* Body -

ответ: json c товарами
  


6 **Карточка товара**\
Get запрос
* url: http://127.0.0.1:8000/product/8-например
* Headers: -
* Body -

ответ: json с товаром с id=8
  

7 **Карзина**\
Get запрос
* url: http://127.0.0.1:8000/my_basket/
* Headers: {Authorization: Token myToken}
* Body -

ответ: json с товарами в карзине текущего юзера

POST запрос
* url: http://127.0.0.1:8000/my_basket/
* Headers: {Authorization: Token myToken}
* Body 
  - product
  - shop
  - quantity

ответ: статус код

Если product и shop не изменились, а quantity новое то препишется только количество

DELETE запрос
* url: http://127.0.0.1:8000/my_basket/
* Headers: {Authorization: Token myToken}
* Body 
  - id

ответ: статус код

Удалит товар из корзины с выбранным id
  



8 **Подтверждение заказа**\
POST запрос
* url: http://127.0.0.1:8000/confirmation/
* Headers: {Authorization: Token myToken}
* Body 
  -  type (num/address(по умолчанию))
  -  value

ответ: карзина товаров которую подтвердии

на email продавцов чьи товары были в карзине улетит сообщение, а так же покупателю на его email
  