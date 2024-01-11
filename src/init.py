# -*- coding: utf-8 -*-

import os
import subprocess

if os.getenv('TESTING') == 'true' and os.getenv('RUN_TESTS_ON_THIS_INSTANCE') == 'true':
    subprocess.call('pytest tests')
if os.getenv('DEVELOPMENT') == 'true':
    subprocess.call(
        f"python -m flask run -h {os.getenv('INSTANCE_HOSTNAME')} "
        f"-p {int(os.getenv('INSTANCE_PORT'))} --debug", shell=True)
else:
    subprocess.call(
        f"uwsgi --http {os.getenv('INSTANCE_HOSTNAME')}:{int(os.getenv('INSTANCE_PORT'))} "
        f"--listen 1000 --http-workers 10 -w app:app", shell=True)
