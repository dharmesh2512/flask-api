import os

SECRET_KEY = os.urandom(64)

# Turns on debugging features in Flask
DEBUG = True
REMOTE_LOGS = False

PROTOCOL = "http"
PORT = 5000
