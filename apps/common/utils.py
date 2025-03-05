import secrets

from apps.common.models import BaseModel


def generate_unique_code(model: BaseModel, field: str) -> str:
    """
        Генерирует уникальный код для указанной модели и поля.

        Args:
            model (BaseModel): Класс модели для проверки на уникальность;
            field (str): Имя поля для проверки на уникальность.

        Returns:
            str: Уникальный код.
    """

    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    unique_code = "".join(secrets.choice(allowed_chars) for _ in range(12))
    code = unique_code
    similar_object_exist = model.objects.filter(**{field: code}).exists()
    if not similar_object_exist:
        return code

    return generate_unique_code(model, field)


def set_dict_attr(obj, data):
    """
    Эта функция позволяет обновлять атрибуты объекта динамически, используя данные из словаря. Это особенно полезно,
    если количество атрибутов, которые нужно обновить, неизвестно заранее или меняется. Вместо множественного
    присваивания user.attr1 = ..., user.attr2 = ... и т.д., используется один вызов set_dict_attr
    """
    for attr, value in data.items():
        setattr(obj, attr, value)

        return obj