# Колокоподібна функція належності
# Bell-shaped membership function

from app.colors import palette
import os
from bokeh.io.export import export_png
from app.browser import BROWSER
from sanic import Blueprint, response
from bokeh.plotting import figure
from bokeh.embed import json_item
import numpy as np
import pathlib
from aiofiles import os as async_os

gbellmf_bp = Blueprint('functions_gbellmf', url_prefix='/gbellmf')


def gbellmf(x, a, b, c):
    def local(lx, la, lb, lc):
        return 1 / (1 + pow(abs((lx - lc) / la), (2 * lb)))

    left_y = np.sort([local(xj, a, b, c) for xj in x], axis=-1, kind="stable")
    right_y = np.flip(np.sort(left_y, axis=-1, kind="stable"))
    y = [*left_y, *right_y]
    return y


@gbellmf_bp.route('/', methods=[
    "POST",
])
async def gbellmf_route(request):
    start, stop = request.json['x'].split(':')
    x = np.linspace(int(start), int(stop))
    a = int(request.json['a'])
    b = int(request.json['b'])
    c = int(request.json['c'])
    y = gbellmf(x, a, b, c)

    p = figure(plot_width=400, plot_height=400)
    p.line(np.linspace(int(start), int(stop), num=100),
           y,
           line_width=2,
           line_color=palette('light').line_color)

    return response.json(json_item(p, "gbellmf"))


@gbellmf_bp.route("/image")
async def gbellmf_image_route(request):
    start, stop = request.args['x'][0].split(':')
    x = np.linspace(int(start), int(stop))
    a = int(request.args['a'][0])
    b = int(request.args['b'][0])
    c = int(request.args['c'][0])
    y = gbellmf(x, a, b, c)

    filename = "gbellmf.png"
    p = figure(plot_width=400, plot_height=400)
    p.line(np.linspace(int(start), int(stop), num=100),
           y,
           line_width=2,
           line_color=palette('light').line_color)
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
