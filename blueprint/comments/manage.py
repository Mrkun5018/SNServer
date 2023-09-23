from blueprint.comments import comments
from utils import respond_handle_wrapper
from flask import request


@comments.route('/push/comments', methods=["POST"])
@respond_handle_wrapper
def fetch_token():
    token = request.json.get("comment", None)
    return {
        "type": "validation" if token == "super-note-edit" else "message"
    }
