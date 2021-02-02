from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security_72 import authenticate, identity

app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)

items = []

jwt = JWT(app, authenticate, identity) #  The JWT will produce a new endpoint http://localhost/auth

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )

    @jwt_required()
    def get(self, name):
        # original codes
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = next(filter(lambda item: item["name"] == name, items), None)

        # return the 200 if the 'item' var is truthy (has value), else if falsy or None result.
        return {"item": item}, 200 if item else 404

    def post(self, name):
        # The condition will execute if the item name has already exists.
        # Status code 400 means a 'BAD REQUEST'
        if next(filter(lambda item: item["name"] == name, items), None):
            return {"message" : "An item with the name '{}' already exists.".format(name)}, 400

        # This is the original line when getting the JSON payload.
        # data = request.get_json()

        data = Item.parser.parse_args()

        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items # This will use the var 'items' list from above.
        # This is going to re-create the 'items' list, excluding the var 'name' being called to delete.
        items = list(filter(lambda item: item["name"] != name, items))
        return {"message": "Item deleted."}

    def put(self, name):
        # This is the original line when getting the JSON payload.
        # data = request.get_json()

        data = Item.parser.parse_args()

        item = next(filter(lambda item: item["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)

        return item

class ItemList(Resource):
    def get(self):
        # Remember to always return a JSON value format, it's a dictionary type in Python.
        # The 'items' variable here is a List type.
        return {"items": items}

# The second argument is the endpoint that we are going to access from the class.
# The second argument is the same thing as defining the Flask decorator's endpoint. ex. @app.route('/sample/endpoint')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, "/items")

app.run(port=5000, debug=True)