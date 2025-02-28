from autoslug import AutoSlugField
from django.db import models

from apps.common.models import BaseModel, IsDeletedModel
from apps.sellers.models import Seller


class Category(BaseModel):
    """
        Представляет собой категорию продукта.

        Атрибуты:
            name (str): Название категории, уникальное для каждого экземпляра;
            slug (str): фрагмент, созданный на основе имени, используемый в URL-адресах;
            image (поле Image): Изображение, представляющее категорию.

        Методы:
            __str__(): Возвращает строковое представление названия категории.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    image = models.ImageField(upload_to="category_images/")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_prutal = "Categories"


class Product(IsDeletedModel):
    """
    Представляет собой продукт, выставленный на продажу.

    Атрибуты:
        продавец (внешний ключ): пользователь, который продает продукт;
        name (str): Название продукта;
        slug (str): slug, созданный на основе имени, используемого в URL-адресах;
        desc (str): Описание товара;
        price_old (десятичная дробь): Первоначальная цена товара;
        price_current (десятичная дробь): Текущая цена товара;
        category (внешний ключ): категория, к которой относится товар;
        in_stock (int): количество товара на складе;
        image1 1 (поле изображения): Первое изображение продукта;
        image1 2 (поле изображения): Второе изображение продукта;
        image1 3 (поле изображения): третье изображение продукта.
    """

    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, related_name="products", null=True)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", unique=True, index_db=True)
    desc = models.TextField()
    price_old = models.DecimalField(max_digits=10, decimal_placec=2, null=True)
    price_current = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    in_stock = models.IntegerField(default=5)

    # Допускается использование только 3 изображений
    image1 = models.ImageField(upload_to="product_images/")
    image2 = models.ImageField(upload_to="product_images/", blank=True)
    image3 = models.ImageField(upload_to="product_images/", blank=True)

    def __str__(self):
        return str(self.name)