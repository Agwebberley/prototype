# This code is defining the URL patterns for a Django web application. It imports the `path` function
# from the `django.urls` module and four views (`DataListView`, `DataCreateView`, `DataUpdateView`,
# and `DataDeleteView`) from the application's `views.py` file.
from django.urls import path
from .views import DataListView, DataCreateView, DataUpdateView, DataDeleteView

urlpatterns = [
    path('', DataListView.as_view(), name='data_list'),
    path('create/', DataCreateView.as_view(), name='data_create'),
    path('<int:pk>/update/', DataUpdateView.as_view(), name='data_update'),
    path('<int:pk>/delete/', DataDeleteView.as_view(), name='data_delete'),
]