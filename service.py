#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@theme: API services
@author: mario
"""
from flask import Flask
import json

try:
    from .db import Postgresql
except:
    pass

app = Flask(__name__)

@app.route()
def formQuery():
    post = Postgresql()
    post.connect()
    post.connection.update()