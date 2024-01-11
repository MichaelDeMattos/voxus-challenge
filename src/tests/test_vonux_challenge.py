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

def test_fetch_valid_data(client):
    # valid request
    resp1 = client.get('/api/sunrise_sunset?type=sunrise&latitude=-23.5653114&longitude=-46.642659')
    assert resp1.status_code == 200
    resp2 = client.get('/api/sunrise_sunset?type=sunset&latitude=-23.5653114&longitude=-46.642659')
    assert resp2.status_code == 200

def test_fetch_invalid_data(client):
    # invalid request
    resp1 = client.get('/api/sunrise_sunset?type=sunrisex&latitude=-23.5653114&longitude=-46.642659')
    assert resp1.status_code == 422
    resp2 = client.get('/api/sunrise_sunset?type=sunsetx&latitude=-23.5653114&longitude=-46.642659')
    assert resp2.status_code == 422

