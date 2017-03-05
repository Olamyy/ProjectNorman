from flask import jsonify


def clean_dict(dict):
    data = dict((key, dict[key] if len(dict[key]) > 1 else dict(key)[0]) for key
        in dict.keys())
    return data


def response_ok(data):
        response = {'status': 'success', 'data': data}
        return response


def response_error(message, error=None):
        response = {'status': 'fail', 'message': message, 'error': error}
        return jsonify(response)
