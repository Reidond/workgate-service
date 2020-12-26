# Колокоподібна функція належності
# Bell-shaped membership function

from sanic import Blueprint, response
from bokeh.plotting import figure
from bokeh.embed import json_item
import numpy as np

gbellmf = Blueprint('functions_gbellmf', url_prefix='/gbellmf')


def gbellmf_fn(x, params):
    assert len(
        params
    ) == 3, 'Generalized membership function must have three parameters.'
    a, b, c = np.asarray(params)
    return 1 / (1 + pow(abs((x - c) / a), (2 * b)))


@gbellmf.route('/', methods=[
    "POST",
])
async def gbellmf_route(request):
    start, stop = request.json['x'].split(':')
    x = np.linspace(int(start), int(stop))
    a = int(request.json['a'])
    b = int(request.json['b'])
    c = int(request.json['c'])

    left_y = np.sort([gbellmf_fn(xj, [a, b, c]) for xj in x],
                     axis=-1,
                     kind="stable")
    right_y = np.flip(np.sort(left_y, axis=-1, kind="stable"))
    y = [*left_y, *right_y]

    p = figure(plot_width=400, plot_height=400)
    p.line(np.linspace(int(start), int(stop), num=100), y, line_width=2)

    return response.json(json_item(p, "gbellmf"))
