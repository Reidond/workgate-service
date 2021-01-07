from sanic import Sanic
from .functions import functions
from sanic_cors import CORS
import os

app = Sanic(__name__)
app.blueprint(functions)
CORS(app, resources={r'/functions/*': {"origins": "*"}})

port = int(os.environ.get("PORT", 3001))
app.run(host='0.0.0.0', port=port, debug=False)
