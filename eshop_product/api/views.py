from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from eshop_account.signals import object_viewed_signal
from eshop_brand.models import Brand
from eshop_product.api.filter import ProductFilter
from eshop_product.api.pagination import CategoryPagination, ProductPagination
from eshop_product.models import Product, Category
from rest_framework import generics, permissions
from django_filters import rest_framework as filters
from eshop_product.api.serializers import (
    ProductSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    BrandDetailSerializer, ProductFavouriteUpdateSerializer,
)


# این از همه بهتر بود و با یک لینک و دو خط  کد همه چیز درست شد هم جزئیات محصول و هم لیست
class ProductListAPIViewSet(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    pagination_class = ProductPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        # add view to product views number
        product.view_count += 1
        product.save()
        #  add this code to record product view in history of users profile
        if self.request.user.is_authenticated:
            object_viewed_signal.send(product.__class__, instance=product, request=request)

        return Response(serializer.data)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, **kwargs):
        cat_title = self.get_object()
        products = Product.objects.filter(category__in=Category.objects.get(title=cat_title) \
                                          .get_descendants(include_self=True))
        filter_products = ProductFilter(self.request.GET, queryset=products)
        serializer = ProductSerializer(filter_products.qs, many=True, context={'request': request})

        return Response(serializer.data)


class BrandDetailAPIViewSet(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer

    def get(self, request, **kwargs):
        brand_title = self.get_object()
        products = Product.objects.filter(brand__in=Brand.objects.filter(title=brand_title))
        filter_products = ProductFilter(self.request.GET, queryset=products)
        serializer = ProductSerializer(filter_products.qs, many=True, context={'request': request})

        return Response(serializer.data)


class ProductFavouriteUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductFavouriteUpdateSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def update(self, request, *args, **kwargs):
        serializer = ProductFavouriteUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user.id
            product = Product.objects.get_by_id(request.data['product_id'])
            if product.favourite.filter(id=self.request.user.id).exists():
                product.favourite.remove(self.request.user)

                return Response(data='remove from favourite')
            else:
                product.favourite.add(self.request.user)
                return Response(data='add to favourite')
        return Response(serializer.data)
