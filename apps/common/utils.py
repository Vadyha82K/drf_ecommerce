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