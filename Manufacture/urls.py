from django.urls import path
from .views import ManufactureList, ManufactureCreate, ManufactureUpdate

urlpatterns = [
    path('', ManufactureList.as_view(), name='manufacture_list'),
    path('create/', ManufactureCreate.as_view(), name='manufacture_create'),
    path('update/<int:pk>/', ManufactureUpdate.as_view(), name='manufacture_update'),
]