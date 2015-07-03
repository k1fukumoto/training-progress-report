from importer import import_cert_and_contact
import web
import json

urls = (
    '/report', 'Report'
)

class Report:
    def GET(self):
        return "OK"

    def POST(self):
        rep = import_cert_and_contact(web.data())
        return json.dumps(rep,indent=4) + "\n"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()