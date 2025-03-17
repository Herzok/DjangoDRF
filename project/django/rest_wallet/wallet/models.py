import uuid
from users.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Wallet(models.Model):
    wallet = models.UUIDField(editable=False, default=uuid.uuid4, verbose_name='Кошелек')
    user = models.OneToOneField(to=User, related_name='OTO_key_User',
                                on_delete=models.CASCADE, verbose_name='Владелец')
    balance = models.IntegerField(verbose_name='Баланс',
                                  validators=[
                                      MinValueValidator(-1000),
                                      MaxValueValidator(1000)
                                  ])

    class Meta:
        ordering = ['user']
