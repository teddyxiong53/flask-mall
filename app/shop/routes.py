from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.shop import bp
from app.models import Product, CartItem, Order, OrderItem, ShippingAddress

@bp.route('/cart')
@login_required
def cart():
    cart_items = current_user.cart_items.all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('shop/cart.html', cart_items=cart_items, total=total)

@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > product.stock:
        flash('商品库存不足')
        return redirect(url_for('main.product', id=product_id))
    
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user=current_user, product=product, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('商品已添加到购物车')
    return redirect(url_for('shop.cart'))

@bp.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'error': '无权限操作'}), 403
    
    quantity = int(request.form.get('quantity', 1))
    if quantity > cart_item.product.stock:
        return jsonify({'error': '库存不足'}), 400
    
    cart_item.quantity = quantity
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        flash('无权限操作')
        return redirect(url_for('shop.cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('商品已从购物车移除')
    return redirect(url_for('shop.cart'))

@bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = current_user.cart_items.all()
    if not cart_items:
        flash('购物车为空')
        return redirect(url_for('shop.cart'))
    
    # 获取收货信息
    recipient_name = request.form.get('recipient_name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    
    if not all([recipient_name, phone, address]):
        flash('请填写完整的收货信息')
        return redirect(url_for('shop.cart'))
    
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    order = Order(buyer=current_user, total_amount=total_amount)
    
    # 创建收货地址
    shipping_address = ShippingAddress(
        recipient_name=recipient_name,
        phone=phone,
        address=address,
        order=order
    )
    
    for cart_item in cart_items:
        if cart_item.quantity > cart_item.product.stock:
            flash(f'{cart_item.product.name} 库存不足')
            return redirect(url_for('shop.cart'))
        
        order_item = OrderItem(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        cart_item.product.stock -= cart_item.quantity
        db.session.add(order_item)
        db.session.delete(cart_item)
    
    db.session.add(order)
    db.session.add(shipping_address)
    db.session.commit()
    flash('订单已创建成功')
    return redirect(url_for('shop.orders'))

@bp.route('/orders')
@login_required
def orders():
    page = request.args.get('page', 1, type=int)
    orders = current_user.orders.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('shop/orders.html', orders=orders)

@bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('无权限查看此订单')
        return redirect(url_for('shop.orders'))
    return render_template('shop/order_detail.html', order=order)