import random
import string

from .models import Customer, Order, OrderItem


def random_generator(size=16, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        device = request.COOKIES.get('deviceID')
        customer, created = Customer.objects.get_or_create(device=device)

    order = Order.objects.filter(customer=customer, complete=False).first()
    if order:
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = ""
        cartItems = ""

    data = {'order': order, 'items': items, 'cartItems': cartItems}
    return data