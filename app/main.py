from sanic import Sanic
from .functions import functions
from sanic_cors import CORS

app = Sanic(__name__)
app.blueprint(functions)
CORS(app, resources=r'/functions/*')

app.run(host='0.0.0.0', port=3001, debug=False)
