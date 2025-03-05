from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils import set_dict_attr
from apps.profiles.serializers import ProfileSerializer


class ProfileView(APIView):
    """
    Представление служит для управления профилем пользователя. Оно обрабатывает HTTP-запросы GET, PUT и DELETE:
    """
    serializer_class = ProfileSerializer


    def get(self, request):
        """
        Этот метод обрабатывает GET-запрос. Он получает данные текущего пользователя (request.user), сериализует их с
        помощью ProfileSerializer, и возвращает сериализованные данные в ответе (HTTP код 200). Этот метод используется
        для получения информации о текущем профиле пользователя.
        """
        user = request.user
        serializer = self.serializer_class(user)

        return Response(data=serializer.data, status=200)


    def put(self, request):
        """
        Этот метод обрабатывает PUT-запрос. Он получает данные текущего пользователя (request.user), сериализует данные
        из запроса (request.data) с помощью ProfileSerializer, проверяет валидность данных
        (serializer.is_valid(raise_exception=True)), обновляет данные пользователя с помощью функции set_dict_attr
        (записывая валидированные данные в объект пользователя), сохраняет изменения в базе данных (user.save()),
        снова сериализует обновленного пользователя и возвращает сериализованные данные. Этот метод предназначен для
        обновления информации в профиле пользователя.
        """
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = set_dict_attr(user, serializer.validated_data)
        user.save()
        serializer = self.serializer_class(user)

        return Response(data=serializer.data)


    def delete(self, request):
        """
        Этот метод обрабатывает DELETE-запрос. Он деактивирует учетную запись пользователя, устанавливая
        user.is_active = False, сохраняет изменения и возвращает сообщение об успешной деактивации. Этот метод
        используется для деактивации учетной записи пользователя.
        """
        user = request.user
        user.is_active = False
        user.save()
        return Response(data={"message": "User Account Deactivated"})