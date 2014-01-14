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


import cgi
import sys

from collections import namedtuple

from kana import *


Ortho = namedtuple('Ortho', ['value', 'rank', 'inflgrps'])


Sense = namedtuple('Sense', ['pos', 'gloss'])


def escape(s, quote=None):
    s = s.encode('UTF-8')
    s = cgi.escape(s)
    return s


class Entry:

    def __init__(self, label, senses, orthos):
        self.label = label
        self.senses = senses
        self.orthos = orthos

        self.headword = self._headword()
        self.section = self._section()

    def _headword(self):
        # Return the first hira/kata-kana word
        for ortho in self.orthos:
            reading = ortho.value
            if reading.startswith(u'っ'):
                reading = reading[1:]
            if is_kana(reading[:2]):
                return reading

        sys.stderr.write('error: cannot determine headword for %s\n  %s\n' % (self.label, '; '.join(self.senses[0].gloss)))
        assert False

    def _section(self):
        # Return the first syllable of the headword

        headword = self.headword

        initial = headword[0]
        if len(headword) > 1 and headword[1] in u'ゃャゅュょョァィゥェォ':
            initial += headword[1]

        return initial

    def remove(self, reading):
        assert isinstance(reading, unicode)
        for i in range(len(self.orthos)):
            ortho = self.orthos[i]
            if ortho.value == reading:
                self.orthos.pop(i)
                return
            else:
                for inflgrp_name, inflgrp_values in ortho.inflgrps.items():
                    if reading in inflgrp_values:
                        inflgrp_values.discard(reading)
                        if not inflgrp:
                            del ortho.inflgrps[inflgrp_name]



def write_index_header(stream):
    stream.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    stream.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    stream.write('<html xmlns:idx="www.mobipocket.com" xmlns:mbp="www.mobipocket.com" xmlns="http://www.w3.org/1999/xhtml">\n')
    stream.write('<head>\n')
    stream.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n')
    stream.write('<link rel="stylesheet" type="text/css" href="style.css"/>\n')
    stream.write('</head>\n')
    stream.write('<body topmargin="0" bottommargin="0" leftmargin="0" rightmargin="0">\n')

def write_index_footer(stream):
    stream.write('<mbp:pagebreak/>\n')

    stream.write('</body>\n')
    stream.write('</html>\n')



def write_index(entries, stream):
    # http://www.mobipocket.com/dev/article.asp?basefolder=prcgen&file=indexing.htm
    # http://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf
    # http://www.klokan.cz/projects/stardict-lingea/tab2opf.py

    # Sort entries alphabetically
    entries.sort(lambda x, y: cmp(x.headword, y.headword))

    prev_section = None

    stream = None

    sections = []
    section_streams = {}

    for entry in entries:
        section = entry.section

        if section != prev_section:
            sys.stderr.write('%s\n' % section)

            try:
                stream = section_streams[section]
            except KeyError:
                sections.append(section)
                filename = 'entry-%s.html' % section
                stream = open(filename, 'wt')
                section_streams[section] = stream
                write_index_header(stream)

            prev_section = section


        stream.write('<idx:entry>\n')
        
        stream.write(' <p class=label>' + escape(entry.label) + '</p>\n')
        assert entry.senses
        
        stream.write(' <ul>\n')
        for sense in entry.senses:
            stream.write(' <li>')
            if sense.pos:
                stream.write('<span class=pos>' + ','.join(sense.pos) + '</span> ')
            stream.write(escape('; '.join(sense.gloss)))
            stream.write('</li>\n')
        stream.write(' </ul>\n')

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

    for stream in section_streams.values():
        write_index_footer(stream)
        stream.close()


    # Write the OPF
    stream = open('jmdict.opf', 'wt')
    stream.write('<?xml version="1.0" encoding="utf-8"?>\n')
    stream.write('<package unique-identifier="uid">\n')
    stream.write('  <metadata>\n')
    stream.write('    <dc-metadata xmlns:dc="http://purl.org/metadata/dublin_core">\n')
    stream.write('      <dc:Identifier id="uid">8FC8AF2ED7</dc:Identifier>\n')
    stream.write('      <dc:Title><h2>JMdict Japanese-English Dictionary</h2></dc:Title>\n')
    stream.write('      <dc:Language>ja</dc:Language>\n')
    stream.write('      <dc:Creator>Electronic Dictionary Research &amp; Development Group</dc:Creator>\n')
    stream.write('      <dc:Date>2013-12-29</dc:Date>\n')
    stream.write('      <dc:Copyrights>2013 Electronic Dictionary Research &amp; Development Group</dc:Copyrights>\n')
    stream.write('    </dc-metadata>\n')
    stream.write('    <x-metadata>\n')
    stream.write('      <output encoding="UTF-8" flatten-dynamic-dir="yes"/>\n')
    stream.write('      <DictionaryInLanguage>ja</DictionaryInLanguage>\n')
    stream.write('      <DictionaryOutLanguage>en</DictionaryOutLanguage>\n')
    stream.write('    </x-metadata>\n')
    stream.write('  </metadata>\n')
    stream.write('  <manifest>\n')
    stream.write('    <item id="cover" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>\n')
    stream.write('    <item id="css" href="style.css" media-type="text/css"/>\n')
    stream.write('    <item id="frontmatter" href="frontmatter.html" media-type="text/x-oeb1-document"/>\n')
    for i in range(len(sections)):
        section = sections[i]
        print section
        stream.write('    <item id="entry-%u" href="entry-%s.html" media-type="text/x-oeb1-document"/>\n' % (i, escape(section, quote=True)))
    stream.write('  </manifest>\n')
    stream.write('\n')
    stream.write('  <spine>\n')
    stream.write('    <itemref idref="frontmatter"/>\n')
    for i in range(len(sections)):
        stream.write('    <itemref idref="entry-%u"/>\n' % i)
    stream.write('  </spine>\n')
    stream.write('  <tours/>\n')
    stream.write('  <guide/>\n')
    stream.write('</package>\n')
