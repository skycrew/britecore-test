#!/usr/bin/env bash

service mysql start && python web/init_db.py && python run.py
