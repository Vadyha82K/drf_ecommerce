from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    """
    Сериализатор предназначен для обработки данных профиля пользователя, а именно:
        - Получения данных профиля: Возвращает first_name, last_name, email, avatar и account_type;
        - Обновления данных профиля: Принимает first_name, last_name и  avatar. А email и account_type не могут
        быть изменены;
    """
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    email = serializers.EmailField(read_only=True)
    avatar = serializers.ImageField(required=False)
    account_type = serializers.CharField(read_only=True)


class ShippingAddressSerializer(serializers.Serializer):
    """
    Сериализатор для работы с адресами
    """
    id = serializers.UUIDField(read_only=True)
    full_name = serializers.CharField(max_length=500)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=12)
    address = serializers.CharField(max_length=1000)
    city = serializers.CharField(max_length=100)
    country = serializers.CharField()
    zipcode = serializers.IntegerField()

