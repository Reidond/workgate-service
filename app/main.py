from sanic import Sanic
from .functions import functions

app = Sanic(__name__)
app.blueprint(functions)

app.run(host='0.0.0.0', port=3001, debug=True)
