#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to generate automatic e-mail signatures.

import os

HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
PASSWORD = os.environ.get("PASSWORD")
PORT = os.environ.get("PORT")
MODE = os.environ.get("MODE")