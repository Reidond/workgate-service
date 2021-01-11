"""
Пірамідальна функція належності
Pyramidal membership function
"""

import numpy as np
from app.colors import palette
import os
from bokeh.io.export import export_png
from app.browser import BROWSER
from sanic import Blueprint, response
from bokeh.plotting import figure
from bokeh.embed import json_item
import pathlib
from aiofiles import os as async_os

trimf_bp = Blueprint('functions_trimf', url_prefix='/trimf')


def trimf(x, params):
    a, b, c = np.asarray(params)
    assert a <= b, 'First parameter must be less than or equal to second parameter.'
    assert b <= c, 'Second parameter must be less than or equal to third parameter.'

    if type(x) is not np.ndarray:
        x = np.asarray([x])

    y = np.zeros(len(x))

    # Left slope
    if a != b:
        index = np.logical_and(a < x, x < b)
        y[index] = (x[index] - a) / (b - a)

    # Right slope
    if b != c:
        index = np.logical_and(b < x, x < c)
        y[index] = (c - x[index]) / (c - b)

    # Center
    y[x == b] = 1

    return y


@trimf_bp.route('/', methods=[
    "POST",
])
async def trimf_route(request):
    start, stop = request.json['x'].split(':')
    x = np.linspace(int(start), int(stop))
    a = int(request.json['a'])
    b = int(request.json['b'])
    c = int(request.json['c'])
    y = trimf(x, [a, b, c])

    p = figure(plot_width=400, plot_height=400)
    p.line(x, y, line_width=2, line_color=palette('light').line_color)

    return response.json(json_item(p, "trimf"))


@trimf_bp.route("/image")
async def trimf_image_route(request):
    start, stop = request.args['x'][0].split(':')
    x = np.linspace(int(start), int(stop))
    a = int(request.args['a'][0])
    b = int(request.args['b'][0])
    c = int(request.args['c'][0])
    y = trimf(x, [a, b, c])

    filename = "trimf.png"
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
