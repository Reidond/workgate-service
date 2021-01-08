from sanic import Blueprint, response

from .gaussmf import gaussmf_bp
from .gbellmf import gbellmf_bp
from .sigmf import sigmf_bp
from .hbmf import hbmf_bp
from .epmf import epmf_bp
from .csmf import csmf_bp

functions = Blueprint.group(gbellmf_bp,
                            gaussmf_bp,
                            sigmf_bp,
                            hbmf_bp,
                            epmf_bp,
                            csmf_bp,
                            url_prefix='/functions')
