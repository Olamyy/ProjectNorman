from flask import Flask
from flask import request
from flask import make_response
from flask_restful import Resource, Api
from core import utils
from core.models import HospitalModel
import os

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class WebHook(Resource):
    def get(self):
        args = request.args
        verify_token = 'python_rocks'

        if args.get('hub.mode') == 'subscribe' and args.get('hub.verify_token') == verify_token:
            print('validating webhook')
            return make_response(args.get('hub.challenge').strip("\n\""))
        else:
            return 'Failed validation. Make sure the validation token match'

    def post(self):
        print(request.args)


class Hospital(Resource):
    def get(self, action, id):
        actions = ['details', 'disable']
        if action not in actions:
            utils.response_error("Invalid Action")
        elif action == "details":
            hospital_data = HospitalModel.objects(name=id)
            if hospital_data:
                return utils.response_ok(hospital_data)
            else:
                return utils.response_error("Unable to retrieve hospital data")
        else:
            pass



api.add_resource(HelloWorld, '/')
api.add_resource(WebHook, '/webhook')
api.add_resource(WebHook, '/hospital/<action>')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
