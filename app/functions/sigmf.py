# Колокоподібна функція належності
# Bell-shaped membership function

import os
from bokeh.io.export import export_png
from app.browser import BROWSER
from sanic import Blueprint, response
from bokeh.plotting import figure
from bokeh.embed import json_item
import numpy as np
import pathlib
from aiofiles import os as async_os

sigmf_bp = Blueprint('functions_sigmf', url_prefix='/sigmf')


def sigmf(x, a, b):
    def local(lx, la, lb):
        return 1 / (1 + pow(np.e, (-la * (lx - lb))))

    if type(x) is not np.ndarray:
        x = np.asarray([x])

    left_y = np.sort([local(xj, a, b) for xj in x], axis=-1, kind="stable")

    return left_y


@sigmf_bp.route('/', methods=[
    "POST",
])
async def sigmf_route(request):
    start, stop = request.json['x'].split(':')
    x = np.linspace(int(start), int(stop))
    a = int(request.json['a'])
    b = int(request.json['b'])
    y = sigmf(x, a, b)

    p = figure(plot_width=400, plot_height=400)
    p.line(x, y, line_width=2)

    return response.json(json_item(p, "sigmf"))


@sigmf_bp.route("/image")
async def sigmf_image_route(request):
    start, stop = request.args['x'][0].split(':')
    x = np.linspace(int(start), int(stop))
    a = int(request.args['a'][0])
    b = int(request.args['b'][0])
    y = sigmf(x, a, b)

    filename = "sigmf.png"
    p = figure(plot_width=400, plot_height=400)
    p.line(x, y, line_width=2)
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
