# -*- coding: utf-8 -*- 
#
# Copyright 2014-2017 Jose Fonseca
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


import sys
import htmlmin

from collections import namedtuple
from html import escape

from kana import *
from cover import *
from pronunciation import format_pronunciations

NAME_ENTRY, VOCAB_ENTRY = range(2)
NAME_INDEX, VOCAB_INDEX = range(2)

Ortho = namedtuple('Ortho', ['value', 'rank','inflgrps'])

Kanji = namedtuple('Kanji', ['keb', 'rank'])

class Reading:
    def __init__(self, reb, rank, re_restr, pronunciation):
        self.reb = reb
        self.rank = rank
        self.re_restr = re_restr
        self.pronunciation = pronunciation

Sense = namedtuple('Sense', ['pos', 'dial', 'gloss', 'misc'])

class Sentence:

    def __init__(self, english, japanese, good_sentence):
        self.english = english
        self.japanese =japanese
        self.good_sentence = good_sentence

class Entry:

    def __init__(self, senses, orthos, kanjis, readings, sentences=None, entry_type=VOCAB_ENTRY):
        self.senses = senses
        self.orthos = orthos
        self.kanjis = kanjis
        self.readings = readings
        self.readings.sort(key=lambda reading:reading.rank)
        self.kanjis.sort(key=lambda kanji:kanji.rank)
        self.orthos.sort(key=lambda ortho:ortho.rank)
        if(sentences == None):
            self.sentences = []
        else:
            self.sentences = sentences

        self.entry_type = entry_type

        self.headword = self._headword()
        self.section = self._section()

    def _headword(self):
        # Return the first hira/kata-kana word
        for ortho in self.orthos:
            reading = ortho.value
            if reading.startswith('っ'):
                reading = reading[1:]
            if is_kana(reading[:2]):
                return reading

        # Fallback to the first reading
        return self.orthos[0].value

    def _section(self):
        # Return the first syllable of the headword

        headword = self.headword

        initial = headword[0]
        if len(headword) > 1 and headword[1] in 'ゃャゅュょョァィゥェォ':
            initial += headword[1]

        return initial

    def remove(self, reading):
        assert isinstance(reading, str)
        for i in range(len(self.orthos)):
            ortho = self.orthos[i]
            if ortho.value == reading:
                self.orthos.pop(i)
                return
            else:
                for inflgrp_name, inflgrp_values in list(ortho.inflgrps.items()):
                    if reading in inflgrp_values:
                        inflgrp_values.discard(reading)
                        if not inflgrp:
                            del ortho.inflgrps[inflgrp_name]



def write_index_header(stream):
    stream.write('<!DOCTYPE html>\n')
    stream.write('<html>\n')
    stream.write('<head>\n')
    stream.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n')
    stream.write('<link rel="stylesheet" type="text/css" href="style.css"/>\n')
    stream.write('</head>\n')
    stream.write('<body topmargin="0" bottommargin="0" leftmargin="0" rightmargin="0">\n')
    stream.write('<mbp:frameset>\n')


def write_index_footer(stream):
    stream.write('<mbp:pagebreak/>\n')
    stream.write('</mbp:frameset>\n')
    stream.write('</body>\n')
    stream.write('</html>\n')

def sort_function(entry):
    if len(entry.kanjis) > 0:
        k_rank = entry.kanjis[0].rank
    else:
        k_rank = 100
    if len(entry.readings) > 0:
        r_rank = entry.readings[0].rank
    else:
        r_rank = 100
    rank =  min(k_rank, r_rank)
    if(entry.entry_type == VOCAB_ENTRY):
        return f"1-{rank}-{entry.headword}"
    else:
        return f"2-{rank}-{entry.headword}"

def write_index(entries, dictionary_name, title, stream, respect_re_restr=True, default_index=VOCAB_INDEX):
    # http://www.mobipocket.com/dev/article.asp?basefolder=prcgen&file=indexing.htm
    # http://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf
    # http://www.klokan.cz/projects/stardict-lingea/tab2opf.py

    # Sort entries alphabetically
    entries.sort(key=sort_function)

    prev_section = None
    dictionary_file_name = dictionary_name.replace(' ', '_')

    stream = None

    sections = []
    section_streams = {}

    for entry in entries:
        section = entry.section

        if section != prev_section:
            try:
                stream = section_streams[section]
            except KeyError:
                sections.append(section)
                filename = 'entry-%s-%s.html'%(dictionary_file_name, section)
                stream = open(filename, 'wt', encoding='UTF-8')
                section_streams[section] = stream
                write_index_header(stream)

            prev_section = section

        #scriptable="yes" is needed, otherwise the results are cut off or results after the actual result are also dsiplayed
        if  default_index != None:
            if entry.entry_type == VOCAB_ENTRY:
                stream.write('<idx:entry name="v" scriptable="yes">\n')
            elif entry.entry_type == NAME_ENTRY:
                stream.write('<idx:entry name="n" scriptable="yes">\n')
            else:
                print(f"Not implemented entry type: {entry.entry_type}")
        else:
            stream.write('<idx:entry scriptable="yes">\n')
        
        assert entry.readings
        if respect_re_restr:
            special_readings = {}
            readings = []
            for reading in entry.readings:
                if reading.re_restr:
                    if(not reading.re_restr in special_readings):
                        special_readings[reading.re_restr] = []
                    special_readings[reading.re_restr].append(reading)
                readings.append(format_pronunciations(reading))
            label = ";".join(readings)
            if entry.kanjis:
                label += '【' + ';'.join([escape(kanji.keb, quote=False) for kanji in entry.kanjis]) + '】'
            
            stream.write(' <p class=lab>' + label + '</p>\n')

            if(len(special_readings.keys()) > 0):
                for kanji in special_readings:
                    label = ""
                    readings = []
                    for reading in special_readings[kanji]:
                        readings.append(format_pronunciations(reading))
                    label = ";".join(readings)
                    label += '【' + escape(kanji, quote=False) + '】'
                    stream.write(' <p class=lab>' + label + '</p>\n')
        else:
            label = ';'.join([reading.reb for reading in entry.readings])
            if entry.kanjis:
                label += '【' + ';'.join([kanji.keb for kanji in entry.kanjis]) + '】'
                    
        assert entry.senses
        
        if(len(entry.senses) > 0):
            stream.write(' <ul>\n')
            for sense in entry.senses:
                stream.write(' <li>')
                if sense.pos or sense.dial or sense.misc:
                    stream.write('<span class=pos>' + ','.join(sense.pos + sense.dial + sense.misc) + '</span> ')
                stream.write(escape('; '.join(sense.gloss), quote=False))
                stream.write('</li>\n')
            stream.write(' </ul>\n')

        if(entry.entry_type == VOCAB_ENTRY and len(entry.sentences) > 0):
            stream.write('<div class=ex>\n')
            stream.write(' <span class="exh">Examples:</span>\n')
            entry.sentences.sort(reverse=True, key = lambda sentence: sentence.good_sentence)
            for sentence in entry.sentences:
                stream.write(' <div class="sen">\n')
                stream.write('  <span>' + sentence.japanese + '</span>\n')
                stream.write('  <br>\n')
                stream.write('  <span>' + sentence.english + '</span>\n')
                stream.write(' </div>\n')
            stream.write('</div>\n')

        for ortho in entry.orthos:
            stream.write(' <idx:orth value="%s"' % escape(ortho.value, quote=True))
            if ortho.inflgrps:
                stream.write('>\n')
                for inflgrp in list(ortho.inflgrps.values()):
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

    for stream in list(section_streams.values()):
        write_index_footer(stream)
        stream.close()

    #create cover
    createCover(dictionary_name, title, 768, 1024)

    # minify html
    minifier = htmlmin.Minifier(remove_empty_space=True)
    for i in range(len(sections)):
        section = sections[i]
        with open('entry-%s-%s.html' %(dictionary_file_name, section), 'r+', encoding='UTF-8') as f:
            content = f.read()
            content = minifier.minify(content)
            f.seek(0)
            f.write(content)
            f.truncate()


    # Write the OPF
    stream = open('%s.opf' %dictionary_file_name, 'wt', encoding='UTF-8')
    stream.write('<?xml version="1.0" encoding="utf-8"?>\n')
    stream.write('<package unique-identifier="uid">\n')
    stream.write('  <metadata>\n')
    stream.write('    <dc-metadata xmlns:dc="http://purl.org/metadata/dublin_core">\n')
    stream.write('      <dc:Identifier id="uid">%s</dc:Identifier>\n' %(hex(hash(title)).split('x')[1]))
    stream.write('      <dc:Title><h2>%s</h2></dc:Title>\n' %title)
    stream.write('      <dc:Language>ja</dc:Language>\n')
    stream.write('      <dc:Creator>Electronic Dictionary Research &amp; Development Group</dc:Creator>\n')
    stream.write('      <dc:Date>2019-05-08</dc:Date>\n')
    stream.write('      <dc:Copyrights>2013 Electronic Dictionary Research &amp; Development Group</dc:Copyrights>\n')
    stream.write('    </dc-metadata>\n')
    stream.write('    <x-metadata>\n')
    stream.write('      <output encoding="UTF-8" flatten-dynamic-dir="yes"/>\n')
    stream.write('      <DictionaryInLanguage>ja</DictionaryInLanguage>\n')
    stream.write('      <DictionaryOutLanguage>en</DictionaryOutLanguage>\n')
    if default_index == VOCAB_INDEX:
        stream.write('  <DictionaryOutLanguage>v</DictionaryOutLanguage>\n')
    elif default_index == NAME_INDEX:
        stream.write('  <DictionaryOutLanguage>n</DictionaryOutLanguage>\n')
    stream.write('    </x-metadata>\n')
    stream.write('  </metadata>\n')
    stream.write('  <manifest>\n')
    stream.write('    <item id="cover" href="%s-cover.jpg" media-type="image/jpeg" properties="cover-image"/>\n' %dictionary_file_name)
    stream.write('    <item id="css" href="style.css" media-type="text/css"/>\n')
    stream.write('    <item id="frontmatter" href="%s-frontmatter.html" media-type="text/x-oeb1-document"/>\n' %dictionary_file_name)
    for i in range(len(sections)):
        section = sections[i]
        stream.write('    <item id="entry-%u" href="entry-%s-%s.html" media-type="text/x-oeb1-document"/>\n' % (i, dictionary_file_name, escape(section, quote=True)))
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
