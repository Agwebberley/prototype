from django.urls import path
from .views import IndexView, LogView

app_name = 'shared'

urlpatterns = [
    path('log/', LogView.as_view(), name='log'),
    path('', IndexView.as_view(), name='index')
]