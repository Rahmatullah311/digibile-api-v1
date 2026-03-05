from ..serializers.coupon_serializer import CouponSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from coupon.models.coupon import Coupon
from rest_framework.permissions import IsAuthenticated
from ..utils import CouponError


class CouponListCreateView(ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]


class CouponRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]
