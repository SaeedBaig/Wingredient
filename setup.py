from setuptools import setup, find_packages

setup(
    name="Wingredient",
    version="0.1.0",
    description="Wingredient",
    packages=find_packages(include=["wingredient", "wingredient.*"]),
    install_requires=["flask>=1.1<=1.2", "flask-mako>=0.4<=1.0"],
    extras_require={"dev": ["black>=19.3b0"]},
    entry_points={"console_scripts": ["wingredient=wingredient.__main__"]},
)
