from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.permissions import IsAdminUser


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'destroy', 'update'):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()
