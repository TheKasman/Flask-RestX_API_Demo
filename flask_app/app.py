from flask import Flask
from flask_restx import Api

from flask_app.resources.items import ns as items_ns

app = Flask(__name__)
api = Api(app, version="1.0", title="RPG Items API", description="Flask-RESTX demo API")

api.add_namespace(items_ns, path="/items")

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000, threads=1)
