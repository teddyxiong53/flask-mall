from flask import render_template, request, current_app
from app.main import bp
from app.models import Product

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    return render_template('main/index.html', products=products)

@bp.route('/product/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    return render_template('main/product.html', product=product)