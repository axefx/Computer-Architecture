#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
if len(sys.argv) > 1:
    print(f"loading: {sys.argv[1]}")
    cpu.load()
else:
    print(len(sys.argv))
    print('Please provide valid filename')
    print('ex. "python3 ls8.py examples/mult.ls8"')
    sys.exit()
cpu.run()