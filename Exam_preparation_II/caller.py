import os
import django
from django.db.models import Q, Count, F

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from populate_db import populate_model_with_data
from main_app.models import Profile, Product, Order


def get_profiles(search_string:str = None):
    if search_string is None:
        return ""

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
            |
        Q(email__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
        for p in profiles
    )

def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    return "\n".join(
        f"Profile: {p.full_name}, orders: {p.orders_count}"
        for p in profiles
    )

def get_last_sold_products() -> str:
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ""

    product_names = [product.name for product in last_order.products.all()]

    return f"Last sold products: {', '.join(product_names)}"

def get_top_products():
    most_sold_products = Product.objects.annotate(
        orders_count=Count('order')
    ).filter(
        orders_count__gt=0
    ).order_by(
        '-orders_count',
        'name'
    )[:5]

    if not most_sold_products:
        return ""

    product_lines = [f"{p.name}, sold {p.orders_count} times" for p in most_sold_products]

    return f"Top products:\n" + "\n".join(product_lines)

def apply_discounts():
    updated_orders = Order.objects.annotate(
        products_count=Count('products')
    ).filter(
        products_count__gt=2,
        is_completed=False,
    ).update(
        total_price=F('total_price') * 0.90
    )
    return f"Discount applied to {updated_orders} orders."

def complete_order() -> str:
    
    order = Order.objects.prefetch_related('products').filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not order:
        return ""

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

        product.save()

    order.is_completed = True
    order.save()

    return f"Order has been completed!"
