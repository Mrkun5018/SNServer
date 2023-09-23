from flask import Blueprint

config = Blueprint('config', __name__, url_prefix='/config')
from . import manage

__all__ = ['config']
