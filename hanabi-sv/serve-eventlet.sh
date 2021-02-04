#!/bin/bash
web: gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 flask-api.main:app
