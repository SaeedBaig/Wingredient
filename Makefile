# Python executable name
PYTHON ?= python3.7

# Style
reformat:  # Project-wide reformat
	$(PYTHON) -m black -l 99 --target-version py37 `git ls-files "*.py"`
stylecheck:  # Check if any files would be reformatted by `make reformat`
	$(PYTHON) -m black --check -l 99 --target-version py37 `git ls-files "*.py"`

# Management of virtual environment
VENV_PATH ?= .venv
_newenv:
	$(PYTHON) -m venv --clear $(VENV_PATH)
	$(VENV_PATH)/bin/pip install -U pip setuptools
newenv: _newenv syncenv  # Set up a fresh Python 3.7 virtual environment
syncenv:  # Install requirements to virtual environment
	$(VENV_PATH)/bin/python -m pip install --upgrade --editable .[dev]
