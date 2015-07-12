from importer import import_cert_and_contact
from flask import Flask, request,Response
from flask_restful import Resource, Api, reqparse
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
api = Api(app)

report_configs = {
  'cert_acronyms': ['VSP','VTSP','VCP6-DCV','VCA-DCV','VSP - CP','VOP-CP'],
  'date_range': {'start': datetime(2013,7,1),
                 'end': datetime(2015,7,1),
                 'step': relativedelta(months=+1)
                 }
}

class Report(Resource):
    def post(self):
        rows = import_cert_and_contact(request.get_data(),report_configs)
        rep = '\n'.join([ ','.join(row) for row in rows]) + '\n'
        return Response(rep,mimetype='Text/plain')

api.add_resource(Report, '/report')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
