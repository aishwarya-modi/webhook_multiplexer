import logging
from flask import jsonify
from constants import RESPONSE_CODE_ERROR, RESPONSE_CODE_NOT_FOUND

class DatabaseError(Exception):
    pass

class NotFoundError(Exception):
    pass

class ForwardingError(Exception):
    pass

def handle_exception(e):
    if isinstance(e, NotFoundError):
        response = {"error": str(e)}, RESPONSE_CODE_NOT_FOUND
    elif isinstance(e, DatabaseError):
        response = {"error": str(e)}, RESPONSE_CODE_ERROR
    elif isinstance(e, ForwardingError):
        response = {"error": str(e)}, RESPONSE_CODE_ERROR
    else:
        response = {"error": "An unexpected error occurred"}, RESPONSE_CODE_ERROR

    logging.error(f"Exception: {str(e)}")
    return jsonify(response[0]), response[1]
