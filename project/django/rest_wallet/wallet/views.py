from rest_framework import generics
from rest_framework.exceptions import APIException, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Wallet
from .serializers import WalletSerializer


class WalletRUApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        data = request.data.copy()
        instance = self.get_wallet()

        data = self.change_balance(data, instance)

        serializer = WalletSerializer(data={'balance': data['amount']}, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        instance = self.get_wallet()

        return Response(WalletSerializer(instance).data)

    def change_balance(self, data, instance):

        try:
            data['amount'] = int(data['amount'])
        except ValueError:
            raise ValidationError("There are non-numeric characters")

        if data['operation'] == 'WITHDRAW':
            data['amount'] = instance.balance - data['amount']
        elif data['operation'] == 'DEPOSIT':
            data['amount'] = instance.balance + data['amount']
        else:
            raise ValidationError("You sent wrong operation")

        return data

    def get_wallet(self):
        instance = Wallet.objects.filter(wallet=self.kwargs.get('uuid_wallet'), user=self.request.user).first()
        if not instance:
            raise NotFound("Wallet not found")
        return instance


class WalletCretaApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if Wallet.objects.filter(user=self.request.user).exists():
            raise ValidationError("Wallet for you exists")

        instance = Wallet.objects.create(user=self.request.user, balance=0)

        return Response(WalletSerializer(instance=instance).data)
