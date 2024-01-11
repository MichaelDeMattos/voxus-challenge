# -*- coding: utf-8 -*-

import os
import uuid

DEVELOPMENT = os.getenv('DEVELOPMENT', False)
SECRET_KEY = os.getenv('SECRET_KEY', str(uuid.uuid4()))
