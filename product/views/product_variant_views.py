from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from product.serializers.product_variant_serializer import ProductVariantSerializer
from product.models.product_variant import ProductVariant
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProductVariantListCreateView(ListCreateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = request.data.copy()
        data["created_by"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
