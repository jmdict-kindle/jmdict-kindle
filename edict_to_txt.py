#!/usr/bin/env python

import gzip
import sys

for arg in sys.argv[1:]:
    sys.stdout.write(gzip.open(arg, 'rb').read().decode('EUC-JP').encode('UTF-8'))
