import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from werkzeug.contrib.fixers import ProxyFix
from resources.user import UserRegister
from resources.item import Item, ItemList
from datetime import timedelta
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # switch off flask-sqlalc_track_modif but not sqlalchemy
app.secret_key = 'somecode'
api = Api(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

jwt = JWT(app, authenticate, identity)  # create /auth

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores/')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
