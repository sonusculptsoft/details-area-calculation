from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)  # Enable CORS for all routes

from polygon_calculation import manage


class MyAPI(Resource):
    def post(self):
        json_data = request.get_json()
        return_response = manage(region_list=json_data.get("region_list"))

        return {"status": "success", "data": return_response}


api.add_resource(MyAPI, "/my-api")

if __name__ == "__main__":
    app.run(debug=True, port=6767, host="0.0.0.0")
