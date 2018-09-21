from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class StoreList(Resource):
    # @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}, 200


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store already exists'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "Error occured while inserting store"}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store {} deleted'.format(name)}