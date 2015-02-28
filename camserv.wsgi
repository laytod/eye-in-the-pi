#!/usr/bin/python
import os
import sys
import logging

logging.basicConfig(stream=sys.stderr)
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir)

from cameraPi import app as application
