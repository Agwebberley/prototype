# This code is defining the URL patterns for a Django web application. It imports the `path` function
# from the `django.urls` module and four views (`DataListView`, `DataCreateView`, `DataUpdateView`,
# and `DataDeleteView`) from the application's `views.py` file.
from django.urls import path
from .views import DataListView, DataCreateView, DataUpdateView, DataDeleteView, LogView, IndexView

urlpatterns = [
    path('customers/', DataListView.as_view(), name='data_list'),
    path('create/', DataCreateView.as_view(), name='data_create'),
    path('customers/<int:pk>/update/', DataUpdateView.as_view(), name='data_update'),
    path('customers/<int:pk>/delete/', DataDeleteView.as_view(), name='data_delete'),
    path('log/', LogView.as_view(), name='log'),
    path('', IndexView.as_view(), name='index'),
]