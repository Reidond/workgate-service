from sanic import Blueprint, response
from .gbellmf import gbellmf

functions = Blueprint.group(gbellmf, url_prefix='/functions')
