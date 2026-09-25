#!/usr/bin/env python3
"""
build_topologies_spec.py - Generates topic_topologies_spec.py with authentic,
per-topic D1, D2, and D3 specifications for all 60 topics.
"""
import os
import json

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topic_topologies_spec.py")

print("Writing topic_topologies_spec.py...")
