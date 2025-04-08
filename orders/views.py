from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from products.models import Product


@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('product_list')

    # Check stock before creating order
    for item in cart.items.all():
        if item.quantity > item.product.stock:
            messages.warning(request, f'Sorry, only {item.product.stock} of {item.product.name} available')
            return redirect('cart_detail')

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')

        if not shipping_address or not payment_method:
            messages.warning(request, 'Please provide shipping address and payment method')
            return redirect('checkout')

        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price,
            shipping_address=shipping_address,
            payment_method=payment_method
        )

        # Create order items and update product stock
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_discounted_price()
            )

            # Update product stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear the cart
        cart.items.all().delete()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def admin_order_list(request):
    if request.user.is_customer:
        return redirect('product_list')

    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/admin_order_list.html', {'orders': orders})


@login_required
def admin_order_detail(request, order_id):
    if request.user.is_customer:
        return redirect('product_list')

    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/admin_order_detail.html', {'order': order})


@login_required
def update_order_status(request, order_id):
    if request.user.is_customer:
        return redirect('product_list')

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated successfully')
        else:
            messages.warning(request, 'Invalid status')

    return redirect('admin_order_detail', order_id=order.id)