# Еліпсоїдна функція належності
# Ellipsoid membership function

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

epmf_bp = Blueprint('functions_epmf', url_prefix='/epmf')


def epmf(x, x0, a):
    res = []
    for xj in x:
        uxj = math.pow(xj - x0, 2) / math.pow(a, 2)
        if uxj < 1:
            res.append(math.sqrt(1 - uxj))
        else:
            res.append(0)
    return res


@epmf_bp.route('/', methods=[
    "POST",
])
async def epmf_route(request):
    start, stop = request.json['x'].split(':')
    x = np.linspace(int(start), int(stop))
    x0 = int(request.json['x0'])
    a = int(request.json['a'])
    y = epmf(x, x0, a)

    p = figure(plot_width=400, plot_height=400)
    p.line(x, y, line_width=2, line_color=palette('light').line_color)

    return response.json(json_item(p, "epmf"))


@epmf_bp.route("/image")
async def epmf_image_route(request):
    start, stop = request.args['x'][0].split(':')
    x = np.linspace(int(start), int(stop))
    x0 = int(request.args['x0'][0])
    a = int(request.args['a'][0])
    y = epmf(x, x0, a)

    filename = "epmf.png"
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
