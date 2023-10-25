from django.urls import path
from my_diplom_app.views import UpdateView, GoodsView, ProductView, BasketView, ConfirmationView



urlpatterns = [
    path('update/', UpdateView.as_view(),),
    path('goods/', GoodsView.as_view(),  name="goods"),
    path('product/<int:id>', ProductView.as_view()),
    path('my_basket/', BasketView.as_view()),
    path('confirmation/', ConfirmationView.as_view()),
]