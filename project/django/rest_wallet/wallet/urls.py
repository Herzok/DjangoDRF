from django.urls import path
from .views import WalletRUApiView,WalletCretaApiView

urlpatterns = [
    path('<uuid:uuid_wallet>', WalletRUApiView.as_view(), name='balance-url'),
    path('create-wallet/', WalletCretaApiView.as_view(), name='create-wallet'),
    path('<uuid:uuid_wallet>/operation', WalletRUApiView.as_view(), name='operations-wallet')
]