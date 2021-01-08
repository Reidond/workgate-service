# Конусоподібна функція належності
# Cone-shaped membership function

from app.colors import palette
import os
from bokeh.io.export import export_png
from app.browser import BROWSER
from sanic import Blueprint, response
from bokeh.plotting import figure
from bokeh.embed import json_item
import numpy as np
import math
import pathlib
from aiofiles import os as async_os

csmf_bp = Blueprint('functions_csmf', url_prefix='/csmf')


def csmf(x, x0, h):
    res = []
    for xj in x:
        ux = math.sqrt(math.pow(xj - x0, 2) / math.pow(h, 2))
        if ux < 1:
            res.append(1 - ux)
        else:
            res.append(0)
    return res


@csmf_bp.route('/', methods=[
    "POST",
])
async def csmf_route(request):
    start, stop = request.json['x'].split(':')
    x = np.linspace(int(start), int(stop))
    x0 = int(request.json['x0'])
    h = int(request.json['h'])
    y = csmf(x, x0, h)

    p = figure(plot_width=400, plot_height=400)
    p.line(x, y, line_width=2, line_color=palette('light').line_color)

    return response.json(json_item(p, "csmf"))


@csmf_bp.route("/image")
async def csmf_image_route(request):
    start, stop = request.args['x'][0].split(':')
    x = np.linspace(int(start), int(stop))
    x0 = int(request.args['x0'][0])
    h = int(request.args['h'][0])
    y = csmf(x, x0, h)

    filename = "csmf.png"
    p = figure(plot_width=400, plot_height=400)
    p.line(x, y, line_width=2, line_color=palette('light').line_color)
    p.toolbar.logo = None
    p.toolbar_location = None
    export_png(p, filename=filename, height=400, width=400, webdriver=BROWSER)

    file_path = os.path.join(pathlib.Path().absolute(), filename)
    file_stat = await async_os.stat(file_path)
    headers = {"Content-Length": str(file_stat.st_size)}

    return await response.file_stream(
        file_path,
        headers=headers,
        chunked=False,
    )
