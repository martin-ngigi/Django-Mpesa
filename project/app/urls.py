from django.urls import path, include
from .views import *
from .payment_views import *

urlpatterns = [
    path('access/token', getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('callback/', MpesaCallBack, name='callback'),
]
