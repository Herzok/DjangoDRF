import uuid

from users.models import User
from .models import Wallet
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse


class WalletTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='zxc123')

        self.wallet = Wallet.objects.create(user=self.user, balance=100)

        self.client = APIClient()
        response = self.client.post('/auth/token/login', {'username': 'testuser', 'password': 'zxc123'}, format='json')
        self.token = response.data['auth_token']
        self.client.force_authenticate(user=self.user, token=self.token)

        self.headers = {
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/json'
        }

    def test_get_wallet(self):
        urls = [
            reverse("balance-url", kwargs={"uuid_wallet": self.wallet.wallet}),
            reverse("balance-url", kwargs={"uuid_wallet": uuid.uuid4()}),
        ]

        response = self.client.get(reverse("balance-url", kwargs={"uuid_wallet": self.wallet.wallet}), **self.headers)
        # test right wallet
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['wallet'], str(self.wallet.wallet))
        self.assertEqual(response.data['balance'], self.wallet.balance)

        response = self.client.get(urls[1], **self.headers)
        # test wrong wallet
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Wallet not found')

    def test_operation_wallet(self):
        urls = [
            reverse("operations-wallet", kwargs={"uuid_wallet": self.wallet.wallet}),
            reverse("operations-wallet", kwargs={"uuid_wallet": uuid.uuid4()}),
        ]

        response = self.client.patch(urls[1], data={'operation': 'sdgdgh', 'amount': '2'}, **self.headers)
        # test wrong wallet
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Wallet not found')

        response = self.client.patch(urls[0], data={'operation': '123', 'amount': '2sdgsgh'},
                                     **self.headers)
        # test wrong type amount
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "There are non-numeric characters")

        response = self.client.patch(urls[0], data={'operation': 'sfsgf', 'amount': '2'}, **self.headers)
        # test wrong type operation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "You sent wrong operation")

        response = self.client.patch(urls[0], data={'operation': 'DEPOSIT', 'amount': '2'}, **self.headers)
        instance = Wallet.objects.get(wallet=self.wallet.wallet, user=self.user)
        # test DEPOSIT opr
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(instance.balance, 102)
        self.assertEqual(instance.user, self.user)
        self.assertEqual(instance.wallet, self.wallet.wallet)

        response = self.client.patch(urls[0], data={'operation': 'WITHDRAW', 'amount': '2'}, **self.headers)
        instance = Wallet.objects.get(wallet=self.wallet.wallet, user=self.user)
        # test WITHDRAW opr after deposit wallet will have 102
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(instance.balance, 100)
        self.assertEqual(instance.user, self.user)
        self.assertEqual(instance.wallet, self.wallet.wallet)

    def test_create_wallet(self):
        response = self.client.post(reverse('create-wallet'), **self.headers)
        # test create wallet
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "Wallet for you exists")

        self.wallet.delete()
        response = self.client.post(reverse('create-wallet'), **self.headers)
        self.wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(self.wallet.wallet), response.data['wallet'])
        self.assertEqual(self.wallet.balance, response.data['balance'])

    def tearDown(self):
        self.wallet.delete()
        self.user.delete()
