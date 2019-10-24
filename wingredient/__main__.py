"""Main module for the wingredient package.

This script is run when you run the `wingredient` command.
"""
from . import db
from .app import run_app
from .config import init_config


try:
    init_config()
    db.init_pool()
    run_app()
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")
finally:
    db.close_pool()
