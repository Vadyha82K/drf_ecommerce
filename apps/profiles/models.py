from django.db import models

from apps.accounts.models import User
from apps.common.models import BaseModel


class ShippingAddress(BaseModel):
    """
        Представляет собой адрес доставки, связанный с пользователем.

        Атрибуты:
            user (ForeignKey): Пользователь, которому принадлежит адрес доставки;
            full_name (str): Полное имя получателя;
            email (str): Адрес электронной почты получателя;
            phone (str): Номер телефона получателя;
            address (str): Уличный адрес получателя;
            city (str): Город получателя;
            country (str): Страна получателя;
            zipcode (in): Почтовый индекс получателя.

        Методы:
            __str__():
                Возвращает строковое представление сведений о доставке.
        """

    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "shipping_addresses"
    )
    full_name = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=1000, null=True)
    city = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    zipcode = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.full_name}'s shipping details"