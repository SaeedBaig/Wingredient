from . import config
from .routes import app

# Necessary for session to work in routes.py
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

def run_app():
    app.run(
        host=config.server.host,
        port=config.server.port,
        debug=True,
    )
