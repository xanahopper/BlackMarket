#!/bin/bash

ps aux | grep python | awk '{print $2;}' | xargs kill -9 2>/dev/null