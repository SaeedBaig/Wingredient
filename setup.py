from setuptools import setup, find_packages

setup(
    name="Wingredient",
    version="0.1.0",
    description="Wingredient",
    # This tells setuptools where to find packages to install. We're simply including the
    # `wingredient` package and all its sub-packages (if any exist).
    packages=find_packages(include=["wingredient", "wingredient.*"]),
    # These are the core dependencies for the application.
    # The reason every dependency *and* all of their sub-dependencies are pinned to specific
    # versions is so we get *deterministic* installations and development environments.
    # Primary dependencies:
    # - Flask
    # - Flask-Mako
    # - Flask-Login
    install_requires=[
        "Click==7.0",
        "Flask==1.1.1",
        "Flask-Mako==0.4",
        "Flask-Login==0.4.1",
        "itsdangerous==1.1.0",
        "Jinja2==2.10.1",
        "Mako==1.1.0",
        "MarkupSafe==1.1.1",
        "psycopg2==2.8.3",
        "Werkzeug==0.16.0",
    ],
    # These are extra/optional requirements which aren't necessary for the application to run, but
    # are used for developing (a.k.a. development tools)
    # Primary dependencies:
    # - black
    extras_require={"dev": ["appdirs==1.4.3", "attrs==19.1.0", "black==19.3b0", "toml==0.10.0"]},
    # This tells setuptools to create a script called `wingredient` which simply runs the
    # `wingredient.__main__` module.
    entry_points={"console_scripts": ["wingredient=wingredient.__main__"]},
)
