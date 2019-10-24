from . import config
from .routes import app


def run_app():
    app.run(
        host=config.server.host,
        port=config.server.port,
        debug=True,
    )
