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
        item = self.find_by_name(name)

        if item:
            return item

        #-- else section isn't needed in the if clause since the method will exit whichever return statement executes.
        return {'message': 'Item not found.'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        #--We are checking if the item already exists to another method because
        #--the 'get' method has the jwt token requirements to be accessed.
        #--The post method has not required a JWT.
        if self.find_by_name(name):
            return {"message" : "An item with the name '{}' already exists.".format(name)}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'],item['price']))
        connection.commit() # You need to commit if you are going to do any changes to the DB table.

        connection.close()

        return item, 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))
        connection.commit()

        connection.close()

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
