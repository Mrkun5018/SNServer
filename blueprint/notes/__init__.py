from flask import Blueprint

notes = Blueprint('notes', __name__, url_prefix='/notes')
from . import manage

__all__ = ['notes']
