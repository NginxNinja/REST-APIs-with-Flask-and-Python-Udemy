from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item

        return {"item": None}, 404

    def post(self, name):
        data = request.get_json()
        # item = {"name": name, "price": 12.00}
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        # Remember to always return a JSON value format, it's a dictionary type in Python.
        # The items variable here is a List type.
        return {"items": items}

# The second argument is the endpoint that we are going to access from the class.
# The second argument is the same thing as defining the Flask decorator's endpoint. ex. @app.route('/sample/endpoint')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, "/items")

app.run(port=5000, debug=True)