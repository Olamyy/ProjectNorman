from flask import Blueprint, jsonify
from flask import make_response
from flask import request
from flask.ext.wtf import CsrfProtect
from flask_restful import Resource

blueprint = Blueprint('api', __name__, url_prefix='/api')


csrf = CsrfProtect()
csrf.exempt(blueprint)


@blueprint.route('/', methods=['GET', 'POST'])
def helloworld():
    view_class = HelloWorld()
    if request.method == "GET":
        return view_class.get()
    else:
        return view_class.post()


class HelloWorld(Resource):
    def get(self):
        return jsonify({'hello': 'world'})

    def post(self):
        return jsonify({'method': 'POST'})


@blueprint.route('/webhook')
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
