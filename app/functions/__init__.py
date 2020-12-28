from sanic import Blueprint, response

from .gaussmf import gaussmf_bp
from .gbellmf import gbellmf_bp

functions = Blueprint.group(gbellmf_bp, gaussmf_bp, url_prefix='/functions')
