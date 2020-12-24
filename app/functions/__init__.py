from sanic import Blueprint

from .gbellmf import gbellmf

functions = Blueprint.group(gbellmf, url_prefix='/functions')
