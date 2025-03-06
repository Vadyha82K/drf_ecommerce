from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sellers.models import Seller
from apps.sellers.serializers import SellerSerializer
from apps.shop.models import Category, Product
from apps.shop.serializers import CreateProductSerializer, ProductSerializer

tags = ["Sellers"]


class SellersView(APIView):
    serializer_class = SellerSerializer

    @extend_schema(
        summary="Apply to become a seller",
        description="""
            Этот endpoint позволяет покупателю подать заявку на то, чтобы стать продавцом.
        """,
        tags=tags)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, partial=False)
        if serializer.is_valid():
            data = serializer.validated_data
            seller, _ = Seller.objects.update_or_create(user=user, defaults=data)
            user.account_type = 'SELLER'
            user.save()
            serializer = self.serializer_class(seller)
            return Response(data=serializer.data, status=201)
        else:
            return Response(data=serializer.errors, status=400)


class ProductsBySellerView(APIView):
    """
    Представление, предназначенно для работы с продуктами конкретного продавца. Оно будет обрабатывать GET-запросы для
    получения списка продуктов продавца и POST-запросы для создания нового продукта.
    """
    serializer_class = ProductSerializer

    @extend_schema(
        summary="Seller Products Fetch",
        description="""
            Этот endpoint возвращает все товары от продавца. 
            Товары могут быть отфильтрованы по названию, размеру или цвету.
        """,
        tags=tags,
    )
    def get(self, request, *args, **kwargs):
        seller = Seller.objects.get_or_none(user=request.user, is_approved=True)
        if not seller:
            return Response(data={"message": "Access is denied"}, status=403)
        products = Product.objects.select_related("category", "seller", "seller__user").filter(seller=seller)
        serializer = self.serializer_class(products, many=True)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Create a product",
        description="""
            Этот endpoint позволяет продавцу создавать продукт.
        """,
        tags=tags,
        request=CreateProductSerializer,
        responses=CreateProductSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateProductSerializer(data=request.data)
        seller = Seller.objects.get_or_none(user=request.user, is_approved=True)
        if not seller:
            return Response(data={"message": "Access is denied"}, status=403)
        if serializer.is_valid():
            data = serializer.validated_data
            category_slug = data.pop("category_slug", None)
            category = Category.objects.get_or_none(slug=category_slug)
            if not category:
                return Response(data={"message": "Category does not exist!"}, status=404)
            data['category'] = category
            data['seller'] = seller
            new_prod = Product.objects.create(**data)
            serializer = self.serializer_class(new_prod)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)