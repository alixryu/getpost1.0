#!/usr/bin/env python3

from getpost import create_app
from getpost.config import DevConfig


app = create_app(DevConfig)
app.run()
