from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity) #  The JWT will produce a new endpoint http://localhost/auth

# The second argument is the endpoint that we are going to access from the class.
# The second argument is the same thing as defining the Flask decorator's endpoint. ex. @app.route('/sample/endpoint')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
