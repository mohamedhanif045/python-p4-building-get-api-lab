from flask import Flask, jsonify, make_response
from models import db, Bakery, BakedGood
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


@app.route('/bakeries')
def get_bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)


@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if not bakery:
        return make_response({"error": "Bakery not found"}, 404)
    bakery_serialized = bakery.to_dict()
    return make_response(jsonify(bakery_serialized), 200)


@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_serialized = [baked_good.to_dict() for baked_good in baked_goods]
    return make_response(jsonify(baked_goods_serialized), 200)


@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not baked_good:
        return make_response({"error": "No baked goods found"}, 404)
    baked_good_serialized = baked_good.to_dict()
    return make_response(jsonify(baked_good_serialized), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
