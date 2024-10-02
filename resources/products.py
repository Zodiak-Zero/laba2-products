from flask_restx import Namespace, Resource, fields
from flask import request

api = Namespace('products', description='Products API')

product_model = api.model('Product', {
    'id': fields.Integer(required=True, description='Product ID'),
    'name': fields.String(required=True, description='Product Name'),
    'manufacturer': fields.String(required=True, description='Manufacturer'),
    'quantity': fields.Integer(required=True, description='Quantity in stock'),
    'price': fields.Float(required=True, description='Product Price'),
    'date_added': fields.String(required=True, description='Date Added (YYYY-MM-DD)'),
})

products = []
next_id = 1

@api.route('/')
class ProductList(Resource):
    @api.marshal_list_with(product_model)
    def get(self):
        """Get list of products"""
        sort_by = request.args.get('sort_by', 'id')
        sorted_products = sorted(products, key=lambda x: x.get(sort_by, 0))
        return sorted_products

    @api.expect(product_model)
    @api.marshal_with(product_model)
    def post(self):
        """Add a new product"""
        global next_id
        new_product = request.json
        new_product['id'] = next_id
        products.append(new_product)
        next_id += 1
        return new_product, 201

@api.route('/<int:id>')
class Product(Resource):
    @api.marshal_with(product_model)
    def get(self, id):
        """Get product by ID"""
        product = next((p for p in products if p['id'] == id), None)
        if product is None:
            api.abort(404, "Product not found")
        return product

    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, id):
        """Update product by ID"""
        product = next((p for p in products if p['id'] == id), None)
        if product is None:
            api.abort(404, "Product not found")
        product.update(request.json)
        return product

    def delete(self, id):
        """Delete product by ID"""
        global products
        products = [p for p in products if p['id'] != id]
        return '', 204

@api.route('/stats')
class ProductStats(Resource):
    def get(self):
        """Get product statistics (average, max, min)"""
        if not products:
            return {"average_price": 0, "max_price": 0, "min_price": 0}

        prices = [p['price'] for p in products]
        return {
            "average_price": sum(prices) / len(prices),
            "max_price": max(prices),
            "min_price": min(prices)
        }
