from importer import import_cert_and_contact
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class Report(Resource):
    def post(self):
        rep = request.get_data()
        rep = import_cert_and_contact(request.get_data())
        return rep

api.add_resource(Report, '/report')

if __name__ == '__main__':
    app.run(debug=True)
