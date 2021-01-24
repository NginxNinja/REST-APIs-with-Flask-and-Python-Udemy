from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
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

        data = request.get_json()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

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