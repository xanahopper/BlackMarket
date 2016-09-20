#!/bin/bash

kill -9 `ps aux |grep gunicorn |grep runserver | awk '{ print $2 }'`
