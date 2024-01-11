# -*- coding: utf-8 -*-

import os
import sys
import pytest
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from app import app as my_app


@pytest.fixture()
def app():
    app = my_app
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
