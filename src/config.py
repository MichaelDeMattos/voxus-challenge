# -*- coding: utf-8 -*-

import os

DEVELOPMENT = os.getenv('DEVELOPMENT')
TESTING = True if os.getenv('TESTING') == 'true' else False
SECRET_KEY = os.getenv('SECRET_KEY')
