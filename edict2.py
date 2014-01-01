#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

#
# Copyright 2014 Jose Fonseca
# All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


import gzip
import re
import sys
import cgi


from dictionary import *



def parse_edict2():
    '''Parse edict2.gz file.
    
    See http://www.edrdg.org/jmdict/edict_doc.html
    '''

    entry_re = re.compile(r'^(\S+) (?:\[(\S+)\] )?/(.+)/(EntL\d+X?)/$')

    entries = []
    for line in gzip.open('edict2.gz', 'rb'):
        line = line.decode('EUC-JP')
        
        if line.startswith(u'　？？？ '):
            # Skip copyright entry -- already included in metadata
            continue
        
        mo = entry_re.match(line)
        assert mo

        kanjis = mo.group(1).split(';')

        if mo.group(2):
            kanas = mo.group(2).split(';')
        else:
            kanas = []

        gloss = mo.group(3).split('/')
    
        try:
            i = gloss.index('(P)')
        except ValueError:
            rank = 1
        else:
            rank = 0
            gloss.pop(i)

        entl = mo.group(4)

        label = u';'.join(kanjis)
        if kanas:
            label += u'【' + u';'.join(kanas) + u'】'

        sense = u'; '.join(gloss)
        senses = [sense]

        orthos = [ortho.split('(')[0] for ortho in kanjis + kanas]

        entry = Entry(label, senses, orthos, rank)

        entries.append(entry)

    return entries


entries = parse_edict2()

entries = prune(entries)

write_index(entries, sys.stdout)


