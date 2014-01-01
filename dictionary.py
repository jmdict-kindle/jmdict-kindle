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


import cgi

from collections import namedtuple


Ortho = namedtuple('Ortho', ['value', 'inflgrps'])


Sense = namedtuple('Sense', ['pos', 'gloss'])


def escape(s, quote=None):
    s = s.encode('UTF-8')
    s = cgi.escape(s)
    return s


class Entry:

    def __init__(self, label, senses, orthos, rank):
        self.label = label
        self.senses = senses
        self.orthos = orthos
        self.rank = rank

    def remove(self, reading):
        for i in range(len(self.orthos)):
            ortho = self.orthos[i]
            if ortho.value == reading:
                self.orthos.pop(i)
            else:
                for inflgrp_name, inflgrp_values in ortho.inflgrps.items():
                    if reading in inflgrp_values:
                        inflgrp_values.discard(reading)
                        if not inflgrp:
                            del ortho.inflgrps[inflgrp_name]


def prune(entries):

    ortho_entry = {}
    for entry in entries:
        orthos = list(entry.orthos)
        for ortho in orthos:
            try:
                prev_entry = ortho_entry[ortho.value]
            except KeyError:
                pass
            else:
                if entry.rank < prev_entry.rank:
                    prev_entry.remove(ortho)
                else:
                    entry.remove(ortho)
                    continue
            ortho_entry[ortho.value] = entry

    # prune entries without orthographies
    # TODO: squash conflicting entries instead of pruning them
    entries = [entry for entry in entries if len(entry.orthos)]

    return entries



def write_index(entries, stream):
    # http://www.mobipocket.com/dev/article.asp?basefolder=prcgen&file=indexing.htm
    # http://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf
    # http://www.klokan.cz/projects/stardict-lingea/tab2opf.py

    stream.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    stream.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    stream.write('<html xmlns:idx="www.mobipocket.com" xmlns:mbp="www.mobipocket.com" xmlns="http://www.w3.org/1999/xhtml">\n')
    stream.write('<head>\n')
    stream.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n')
    stream.write('<link rel="stylesheet" type="text/css" href="style.css"/>\n')
    stream.write('</head>\n')
    stream.write('<body topmargin="0" bottommargin="0" leftmargin="0" rightmargin="0">\n')
    stream.write('<mbp:pagebreak/>\n')

    for entry in entries:
        stream.write('<idx:entry>\n')
        stream.write(' <p><b>' + escape(entry.label) + '</b></p>\n')
        for sense in entry.senses:
            s = '; '.join(sense.gloss)
            if sense.pos:
                s = '(' + ','.join(sense.pos) + ') ' + s
            stream.write(' <p>' + escape(s) + '</p>\n')
        for ortho in entry.orthos:
            stream.write(' <idx:orth value="%s"' % escape(ortho.value, quote=True))
            if ortho.inflgrps:
                stream.write('>\n')
                for inflgrp in ortho.inflgrps.values():
                    assert inflgrp
                    stream.write('  <idx:infl>\n')
                    iforms = list(inflgrp)
                    iforms.sort()
                    for iform in iforms:
                        stream.write('   <idx:iform value="%s"/>\n' % escape(iform, quote=True))
                    stream.write('  </idx:infl>\n')
                stream.write(' </idx:orth>\n')
            else:
                stream.write('/>\n')
        stream.write('</idx:entry>\n')
        stream.write('<hr/>\n')

    stream.write('</body>\n')
    stream.write('</html>\n')
