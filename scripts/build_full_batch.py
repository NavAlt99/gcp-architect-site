#!/usr/bin/env python3
"""
build_full_batch.py - Generates topics for Phase 0 (001-006) and Phase 1 (007-012)
and Phase 2 Core Services (013-021) in full compliance with the Style Lock.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page

def build_topic_batch(topics_list):
    for t in topics_list:
        build_topic_page(t)

print("Batch builder loaded.")
