.PHONY: all install build flake8 distclean

all: .venv

.venv:
	pipenv install --dev

install: dist/switchbot_sdk-0.0.1-py3-none-any.whl
	pipenv run pip install $<

build dist/switchbot_sdk-0.0.1-py3-none-any.whl: .venv
	pipenv run python setup.py bdist_wheel

flake8: .venv
	pipenv run flake8 switchbot examples setup.py

distclean:
	-rm -rf .venv build dist switchbot_sdk.egg-info
