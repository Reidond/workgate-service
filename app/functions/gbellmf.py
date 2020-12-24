# Колокоподібна функція належності
# Bell-shaped membership function

from sanic import Blueprint, response
import json
import io

gbellmf = Blueprint('functions_gbellmf', url_prefix='/gbellmf')


@gbellmf.route('/', methods=[
    "POST",
])
async def gbellmf_route(request):
    data = json.load(io.BytesIO(request.body))
    return response.json(data)
