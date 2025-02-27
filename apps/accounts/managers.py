from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):
    """
    Расширяет стандартную функциональность для создания пользователей, добавляя валидацию данных и специфическую
    логику для суперпользователей.
    """

    def email_validator(self, email):
        """
        Метод проверяет корректность адреса электронной почты с помощью validate_email из django.core.validators
        """
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Вы должны указать действительный адрес электронной почты")

    def validate_user(self, first_name, last_name, email):
        """
        Метод валидирует данные для создания обычного пользователя. Проверяет, что указаны имя, фамилия и корректный
        адрес электронной почты.
        """
        if not first_name:
            raise ValueError("Пользователи должны указать свое имя")

        if not last_name:
            raise ValueError("Пользователи должны указать свою фамилию")

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)

        else:
            raise ValueError("Базовая учетная запись пользователя: Требуется адрес электронной почты")

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        """
        Метод создает обычного пользователя.
        """
        self.validate_user(first_name, last_name, email)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        user.save()
        return user

    def validate_superuser(self, email, password, **extra_fields):
        """
        Метод валидирует данные для создания суперпользователя.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("У суперпользователей должно быть значение is_staff=True")

        if not password:
            raise ValueError("У суперпользователей должен быть пароль")

        if email:
            email = self.normalize_email(email)
            self.email_validate(email)
        else:
            raise ValueError("Учетная запись администратора: Требуется адрес электронной почты")

        return extra_fields

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields = self.validate_superuser(email, password, **extra_fields)
        user = self.create_user(first_name, last_name, email, password, **extra_fields)
        return user
