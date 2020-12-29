from bokeh.embed import json_item
from bokeh.plotting import figure
from sanic import Blueprint, response
import numpy as np
from bokeh.io import export_png
from aiofiles import os as async_os
import pathlib
import os

gaussmf_bp = Blueprint('functions_gaussmf', url_prefix='/gaussmf')


def gaussmf(x, a, b):
    def local(lx, la, lb):
        return np.exp(-pow((lx - lb), 2) / (2 * pow(la, 2)))

    left_y = np.sort([local(xj, a, b) for xj in x], axis=-1, kind="stable")
    right_y = np.flip(np.sort(left_y, axis=-1, kind="stable"))
    y = [*left_y, *right_y]
    return y


@gaussmf_bp.route('/', methods=[
    "POST",
])
async def gaussmf_route(request):
    start, stop = request.json['x'].split(':')
    x = np.linspace(int(start), int(stop))
    a = int(request.json['a'])
    b = int(request.json['b'])
    y = gaussmf(x, a, b)

    p = figure(plot_width=400, plot_height=400)
    p.line(np.linspace(int(start), int(stop), num=100), y, line_width=2)

    return response.json(json_item(p, "gaussmf"))


@gaussmf_bp.route("/image")
async def gaussmf_image_route(request):
    start, stop = request.args['x'][0].split(':')
    x = np.linspace(int(start), int(stop))
    a = int(request.args['a'][0])
    b = int(request.args['b'][0])
    y = gaussmf(x, a, b)

    filename = "gaussmf.png"
    p = figure(plot_width=400, plot_height=400)
    p.line(np.linspace(int(start), int(stop), num=100), y, line_width=2)
    export_png(p, filename=filename, height=400, width=400)

    file_path = os.path.join(pathlib.Path().absolute(), filename)
    file_stat = await async_os.stat(file_path)
    headers = {"Content-Length": str(file_stat.st_size)}

    return await response.file_stream(
        file_path,
        headers=headers,
        chunked=False,
    )
