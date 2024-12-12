from flask import jsonify


class InvalidRequest(Exception):
    def __init__(self, message):
        self.message = message

def sanitize_body(request, required_params):
    body = request.get_json()

    missing_params = []
    for param in required_params:
        if param not in body:
            missing_params.append(param)
    
    if len(missing_params) > 0:
        raise InvalidRequest(f"Missing parameters: {', '.join(missing_params)}")
    
    return body

def send_response(status=200, message="Success", data=None):
    response = jsonify({
        "metadata": {
            "status": status,
            "success": status < 300,
            "message": message
        },
        "data": data
    })

    return response , status