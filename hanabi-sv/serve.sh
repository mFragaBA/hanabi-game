#!/bin/bash
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8080 flask-api.main:app
