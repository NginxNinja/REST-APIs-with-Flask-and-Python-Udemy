import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

        #-- else section isn't needed in the if clause since the method will exit whichever return statement executes.
        return {'message': 'Item not found.'}, 404

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
