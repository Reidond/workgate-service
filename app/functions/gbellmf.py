# Колокоподібна функція належності
# Bell-shaped membership function

from sanic import Blueprint, response
import json
import io
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
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
    data = json.load(io.BytesIO(request.body))

    start, stop = data['x'].split(':')
    x = np.linspace(start, stop)

    left_y = np.sort(
        [gbellmf_fn(xj, [data['a'], data['b'], data['c']]) for xj in x],
        axis=-1,
        kind="stable")
    right_y = np.flip(np.sort(left_y, axis=-1, kind="stable"))
    y = [*left_y, *right_y]

    p = figure(plot_width=400, plot_height=400)
    p.line(args=[np.linspace(start, stop, num=100), y],
           kwargs={'line_width': 2})
    html = file_html(p, CDN, "gbellmf")
    return response.html(html)
