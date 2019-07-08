#!/bin/bash
celery -A lg worker -l info >> /tmp/celery.log