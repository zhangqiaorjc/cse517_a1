# -*- coding: utf-8 -*-

from lm_common import *
import codecs
import sys
import glob
import os.path

import os
from os.path import join, getsize

assert(len(sys.argv) == 2)

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

for root, dirs, files in os.walk(sys.argv[1]):
    for fname in files:
	f = os.path.join(root, fname)
	print f
	raw_text = codecs.open(f, encoding='utf-8', mode='r').read()
	sys.stdout.write(raw_text + EOT)
