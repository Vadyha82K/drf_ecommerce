import uuid

from django.db import models

from apps.common.managers import GetOrNoneManager


class BaseModel(models.Model):
    """
        Базовый класс модели, который включает в себя общие поля и методы для всех моделей.

        Attributes:
            id (UUIDField): Уникальный идентификатор экземпляра модели.
            created_at (DateTimeField): Отметка времени, когда экземпляр был создан.
            updated_at (DateTimeField): Отметка времени последнего обновления экземпляра.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GetOrNoneManager()

    class Meta:
        abstract = True