from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_password(self, value: str) -> str:
        return make_password(value)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Класс служит для добавления данных в payload токена, который создается с помощью TokenObtainPairView
    """
    @classmethod
    def get_token(cls, user):
        """
        Метод сериализатора, который добавляет информацию о группе и роли пользователя в полезную нагрузку токенов
        (refresh и access)
        """
        token = super().get_token(user)

        # Добавляем пользовательские данные в полезную нагрузку
        if user.is_staff:
            token['group'] = 'admin'
        else:
            token['group'] = 'user'
            token['role'] = user.account_type

        return token