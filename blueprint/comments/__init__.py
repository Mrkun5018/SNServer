from flask import Blueprint

comments = Blueprint('comments', __name__, url_prefix='/comments')
from . import manage

__all__ = ['comments']
