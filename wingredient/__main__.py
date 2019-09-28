"""Main module for the wingredient package.

This script is run when you run the `wingredient` command.
"""
from .app import app

try:
    app.run()
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")
