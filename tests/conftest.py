from importlib import import_module
import pytest
import os
import sys
from flask import Flask

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

module_name = "routes"
def make_app():
    mod = import_module(module_name)

    if hasattr(mod, "create_app"):
        app = mod.create_app({"TESTING": True})
        return app
    if hasattr(mod, "app"):
        app = getattr(mod, "app")
        app.config.update(TESTING=True)
        return app

    app = Flask(__name__)
    app.config.update(TESTING=True)

    if hasattr(mod, "api_bp"):
        app.register_blueprint(getattr(mod, "api_bp"))
    else:
        raise RuntimeError(
            f"No se encontró create_app, app ni api_bp en el módulo '{module_name}'. Actualiza module_name en tests/conftest.py"
        )

    return app

@pytest.fixture
def app():
    return make_app()

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def mod():
    """Devuelve el módulo que contiene los endpoints para hacer monkeypatch fácilmente."""
    return import_module(module_name)