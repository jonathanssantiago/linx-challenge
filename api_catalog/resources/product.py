from flask_restful import Resource
from models.product import ProductModel
import json
import os
from app import redis

class Product(Resource):
    def get(self, product_id):
        if redis.get('catalog.product-' + str(product_id)) != None:
            return json.loads(redis.get('catalog.product-' + str(product_id))), 201

        product = ProductModel.get_product(product_id)

        if (product == None):
            return {'message': 'Product not found.'}, 404

        product.pop('_id')

        compact = {
            'name': product['name'],
            'price': product['price'],
            'status': product['status'],
            'categories': product['categories'],
        }

        redis.set(
            'catalog.product-' + str(product_id),
            json.dumps({'complete': product, 'compact': compact}),
            ex=(60 * int(os.environ["CACHE_CATALOG_PRODUCTS_EXPIRE"]))
        )

        return {"compact": compact, "complete": product}, 200
