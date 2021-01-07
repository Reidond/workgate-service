# Гіперболоїдна функція належності
# Hyperboloid membership function

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

hbmf_bp = Blueprint('functions_hbmf', url_prefix='/hbmf')


def hbmf(x, x0, a):
    res = []
    for xj in x:
        ux = math.sqrt(1 + (math.pow(xj - x0, 2) / math.pow(a, 2)))
        if ux < 2:
            res.append(2 - ux)
        else:
            res.append(0)
    return res


@hbmf_bp.route('/', methods=[
    "POST",
])
async def hbmf_route(request):
    start, stop = request.json['x'].split(':')
    x = np.linspace(int(start), int(stop))
    x0 = int(request.json['x0'])
    a = int(request.json['a'])
    y = hbmf(x, x0, a)

    p = figure(plot_width=400, plot_height=400)
    p.line(x, y, line_width=2)

    return response.json(json_item(p, "hbmf"))


@hbmf_bp.route("/image")
async def hbmf_image_route(request):
    start, stop = request.args['x'][0].split(':')
    x = np.linspace(int(start), int(stop))
    x0 = int(request.args['x0'][0])
    a = int(request.args['a'][0])
    y = hbmf(x, x0, a)

    filename = "hbmf.png"
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
