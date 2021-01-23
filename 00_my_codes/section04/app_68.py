from flask import Flask
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
        item = {"name": name, "price": 12.00}
        items.append(item)
        return item, 201

# The second argument is the endpoint that we are going to access from the class.
# The second argument is the same thing as defining the Flask decorator's endpoint. ex. @app.route('/sample/endpoint')
api.add_resource(Item, '/item/<string:name>')

app.run(port=5000)