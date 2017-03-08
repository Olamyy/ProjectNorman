import requests
from flask import Blueprint, jsonify
from flask import json
from flask import make_response
from flask import request
from flask_restful import Resource
from Norman.extensions import csrf_protect

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/', methods=['GET', 'POST'])
@csrf_protect.exempt
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


@blueprint.route('/webhook', methods=['GET', 'POST'])
@csrf_protect.exempt
def webhook():
    view_class = WebHook()
    if request.method == "GET":
        return view_class.get()
    else:
        return view_class.post()


class WebHook(Resource):
    def get(self):
        args = request.args
        verify_token = 'python_rocks'
        if args.get('hub.mode') == 'subscribe' and args.get('hub.verify_token') == verify_token:
            print('validating webhook')
            return make_response(args.get('hub.challenge').strip("\n\""))
        else:
            print('Failed validation. Make sure the validation tokens match')

    def post(self):
        data = request.get_json()
        print(data)
        if data.get('object', None) == 'page':
            message_entries = data['entry']
            for entry in message_entries:
                pageID = entry['id']
                timeOfEvent = entry['time']
                for event in entry['messaging']:
                    if event.get('message', None):
                        self.reply(event)

    def reply(self, event):
        senderID = event['sender']['id']
        recipientID = event['recipient']['id']
        timeOfMessage = event['timestamp']
        message = event['message']

        messageId = message['mid']
        messageText = message.get('text', None)
        messageAttachments = message.get('attachments', None)

        if messageText:
            if messageText == 'generic':
                self.sendGenericMessage(senderID)
            else:
                self.sendTextMessage(senderID, messageText)
        elif messageAttachments:
            print("message with attachement received")
            self.sendTextMessage(senderID, messageText)

    def sendGenericMessage(self, recipientID):
        pass

    def sendTextMessage(self, recipientID, messageText):
        messageDataDict = {'recipient': {'id': recipientID}, 'message': {'text': messageText}}
        messageData = json.dumps(messageDataDict)
        self.callSendAPI(messageData)

    def callSendAPI(self, message):
        access_token = 'EAAS0PtgoBk4BAAV6pDrocKGlPOAjdxynxBidP5noah1l27yRu2x0zZAc1clvjQN1YAY9dHgJKGd8fPqjwHBxQ0KuQxUahCkxUDmecH9OQvAk8FKuZBZA2jQhHPihh85WcALD8UZBMRxYXT1iAqaAGdpUcjKAlOBwL6VwisVC8QZDZD'
        uri = 'https://graph.facebook.com/v2.6/me/messages/access_token=' + access_token
        resp = requests.post(uri, json=message)
        print(resp.status_code, '\n')
        print(resp.text)


