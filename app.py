from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'somecode'
api = Api(app)

jwt = JWT(app, authenticate, identity) # create /auth

items = []


class ItemList(Resource):
    def get(self):
        return {'Items': items}


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'Item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': 'Item is already exists'}
        data = request.get_json()
        new_item = {'name': name, 'price': data['price']}

        items.append(new_item)
        return new_item, 201

    def put(self, name):
        return

    def delete(self, name):
        global items
        items = [item for item in items if item['name'] != name]


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(debug=True)
