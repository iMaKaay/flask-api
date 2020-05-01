from flask import (make_response, jsonify, Response)


class MakeResponse:
    @staticmethod
    def success(data=None, message='', success=True, code=200) -> Response:
        return make_response(jsonify({
            'data': data,
            'message': message,
            'success': success,
        }), code)

    @staticmethod
    def error(message, success=False, code=400) -> Response:
        return make_response(jsonify({
            'message': message,
            'success': success,
        }), code)
