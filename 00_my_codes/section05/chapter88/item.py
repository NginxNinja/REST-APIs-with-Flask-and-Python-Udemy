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
        if Item.find_by_name(name):
            return {"message" : "An item with the name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        # There could be an unforeseen problem in inserting data in the database.
        try:
            self.insert(item)
        except:
            return{"message": "An error occurred inserting the item."}, 500 # Internal Server Error

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'],item['price']))
        connection.commit() # You need to commit if you are going to do any changes to the DB table.

        connection.close()

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

        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data["price"]}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500 # Internal Server Error
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}, 500 # Internal Server Error

        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit() # You need to commit if you are going to do any changes to the DB table.

        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close()

        return {"items": items}
