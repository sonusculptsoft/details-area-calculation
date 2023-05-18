from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

from polygon_calculation import manage


class MyAPI(Resource):
    def post(self):
        json_data = request.get_json()
        return_response = manage(region_list=json_data.get("region_list"))

        return {"status": "success", "data": return_response}


api.add_resource(MyAPI, "/my-api")

if __name__ == "__main__":
    app.run(debug=True)
