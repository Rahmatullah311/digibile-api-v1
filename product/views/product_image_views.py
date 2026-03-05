from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from product.models.product import Product
from product.serializers.product_image_serializer import (
    ProductImageSerializer,
    ProductImageUploadSerializer,
)
from product.models.product_image import ProductImage


class ProductImageListCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        images = product.images.all()  # Related name in ProductImage model
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductImageUploadSerializer(
            data=request.data, context={"product": product}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Images uploaded successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImageRetrieveUpdateDestroyAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk, image_id):
        product_image = ProductImage.objects.get(id=image_id, product__id=pk)
        serializer = ProductImageSerializer(product_image)
        return Response(serializer.data)

    def put(self, request, pk, image_id):
        product_image = ProductImage.objects.get(id=image_id, product__id=pk)
        serializer = ProductImageUploadSerializer(
            product_image, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Image updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, image_id):
        product_image = ProductImage.objects.get(id=image_id, product__id=pk)
        serializer = ProductImageUploadSerializer(
            product_image, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Image partially updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, image_id):
        product_image = ProductImage.objects.get(id=image_id, product__id=pk)
        product_image.delete()
        return Response(
            {"detail": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
