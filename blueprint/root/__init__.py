from flask import Blueprint

root = Blueprint('root', __name__, url_prefix='/')
from . import manage

__all__ = ['root']
