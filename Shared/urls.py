from django.urls import path
from .views import IndexView, LogView

urlPatterns = [
    path('log/', LogView.as_view(), name='log'),
    path('', IndexView.as_view(), name='index')
]