from django.db import transaction
from django.utils import timezone
from django.db.models import Q, F, OuterRef

from decimal import Decimal
from .models import Coupon, CouponUsage, CouponProduct, CouponCategory, CouponStore


class CouponError(Exception):
    """Custom exception for coupon validation errors."""

    pass


def get_applicable_coupons_for_product(product, user=None):
    """
    Return all active coupons that apply to a given product.
    Optionally filter out coupons the user already used.
    """
    now = timezone.now()
    qs = (
        Coupon.objects.filter(
            active=True,
            valid_from__lte=now,
            valid_to__gte=now,
        )
        .filter(
            Q(applicable_to_all=True)
            | Q(coupon_products__product=product)
            | Q(coupon_categories__category=product.category)
            | Q(coupon_stores__store=getattr(product, "store", None))
        )
        .distinct()
    )

    if user:
        qs = qs.exclude(couponusage__user=user, couponusage__coupon=OuterRef("pk"))

    return qs


def validate_coupon_for_order(user, code, products, total_amount):
    """
    Validate a coupon code for the given order.
    - Checks active status, validity dates, usage limits, and applicability.
    - Returns discount value and messages.
    """
    try:
        coupon = Coupon.objects.get(code__iexact=code)
    except Coupon.DoesNotExist:
        raise CouponError("Invalid coupon code.")

    # Check if coupon is valid globally
    if not coupon.is_valid():
        raise CouponError("Coupon expired or inactive.")

    # Check if user already used it
    if (
        CouponUsage.objects.filter(user=user, coupon=coupon).count()
        >= coupon.per_user_limit
    ):
        raise CouponError("You have already used this coupon.")

    # Check usage limit
    if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
        raise CouponError("Coupon usage limit reached.")

    # Check minimum purchase
    if total_amount < coupon.min_purchase:
        raise CouponError(
            f"Minimum order value for this coupon is {coupon.min_purchase}."
        )

    # Check applicability
    applicable_products = []
    for product in products:
        if is_coupon_applicable_to_product(coupon, product):
            applicable_products.append(product)

    if not applicable_products:
        raise CouponError("Coupon not applicable to selected products.")

    # Calculate discount
    discount = calculate_discount(coupon, total_amount)

    return {
        "valid": True,
        "discount": discount,
        "coupon": coupon,
        "applicable_products": applicable_products,
    }


def is_coupon_applicable_to_product(coupon, product):
    """
    Determine if the coupon applies to the given product.
    Works with dedicated relation models.
    """
    if coupon.applicable_to_all:
        return True

    if CouponProduct.objects.filter(coupon=coupon, product=product).exists():
        return True

    if CouponCategory.objects.filter(coupon=coupon, category=product.category).exists():
        return True

    if (
        hasattr(product, "store")
        and CouponStore.objects.filter(coupon=coupon, store=product.store).exists()
    ):
        return True

    return False


def calculate_discount(coupon, total_amount):
    """
    Calculate the discount based on type and value.
    """
    total_amount = Decimal(total_amount)
    if coupon.discount_type == Coupon.PERCENTAGE:
        return (total_amount * coupon.discount_value / 100).quantize(Decimal("0.01"))
    return min(total_amount, coupon.discount_value).quantize(Decimal("0.01"))


@transaction.atomic
def mark_coupon_used(user, coupon):
    """
    Record coupon usage and increment usage counter atomically.
    """
    usage, created = CouponUsage.objects.get_or_create(user=user, coupon=coupon)
    if not created:
        raise CouponError("This coupon has already been used by the user.")

    coupon.used_count = F("used_count") + 1
    coupon.save(update_fields=["used_count"])
    return usage
