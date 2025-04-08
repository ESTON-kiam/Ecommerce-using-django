from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if product.stock <= 0:
        messages.warning(request, 'This product is out of stock!')
        return redirect('product_list')

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Added another {product.name} to your cart')
        else:
            messages.warning(request, f'Cannot add more {product.name} to cart. Only {product.stock} available.')

    return redirect('cart_detail')


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, f'Removed one {product.name} from your cart')
        else:
            cart_item.delete()
            messages.success(request, f'Removed {product.name} from your cart')
    except CartItem.DoesNotExist:
        messages.warning(request, 'This item is not in your cart')

    return redirect('cart_detail')


@login_required
def delete_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f'Removed {product.name} from your cart')
    except CartItem.DoesNotExist:
        messages.warning(request, 'This item is not in your cart')

    return redirect('cart_detail')