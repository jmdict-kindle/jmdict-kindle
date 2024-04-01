# -*- coding: utf-8 -*-
#
# Copyright 2011-2017 Jose Fonseca
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
import gzip
import xml.parsers.expat

from kana import *
from dictionary import *
from inflections import *
from exampleSentences import *
from pronunciation import Pronunciation
import argparse
from types import SimpleNamespace


# limit the number of entries for quick experiments
MAX_ENTRIES = sys.maxsize

XML_ELEMENT_START, XML_ELEMENT_END, XML_CHARACTER_DATA, XML_EOF = range(4)


class XmlToken:
    def __init__(self, type, name_or_data, attrs=None, line=None, column=None):
        assert type in (XML_ELEMENT_START, XML_ELEMENT_END, XML_CHARACTER_DATA, XML_EOF)
        self.type = type
        self.name_or_data = name_or_data
        self.attrs = attrs
        self.line = line
        self.column = column

    def __str__(self):
        if self.type == XML_ELEMENT_START:
            return "<" + self.name_or_data + " ...>"
        if self.type == XML_ELEMENT_END:
            return "</" + self.name_or_data + ">"
        if self.type == XML_CHARACTER_DATA:
            return self.name_or_data
        if self.type == XML_EOF:
            return "end of file"
        assert 0


class XmlTokenizer:
    """Expat based XML tokenizer."""

    def __init__(self, fp, skip_ws=True):
        self.fp = fp
        self.tokens = []
        self.index = 0
        self.final = False
        self.skip_ws = skip_ws
        self.entities = {}

        self.character_pos = 0, 0
        self.character_data = ""

        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.StartElementHandler = self.handle_element_start
        self.parser.EndElementHandler = self.handle_element_end
        self.parser.CharacterDataHandler = self.handle_character_data
        self.parser.EntityDeclHandler = self.handle_entity_decl_handler
        self.parser.SetParamEntityParsing(
            xml.parsers.expat.XML_PARAM_ENTITY_PARSING_NEVER
        )

    def handle_element_start(self, name, attributes):
        self.finish_character_data()
        line, column = self.pos()
        token = XmlToken(XML_ELEMENT_START, name, attributes, line, column)
        self.tokens.append(token)

    def handle_element_end(self, name):
        self.finish_character_data()
        line, column = self.pos()
        token = XmlToken(XML_ELEMENT_END, name, None, line, column)
        self.tokens.append(token)

    def handle_character_data(self, data):
        if not self.character_data:
            self.character_pos = self.pos()
        self.character_data += data

    def handle_entity_decl_handler(
        self,
        entityName,
        is_parameter_entity,
        value,
        base,
        systemId,
        publicId,
        notationName,
    ):
        self.entities[value] = entityName

    def finish_character_data(self):
        if self.character_data:
            if not self.skip_ws or not self.character_data.isspace():
                line, column = self.character_pos
                token = XmlToken(
                    XML_CHARACTER_DATA, self.character_data, None, line, column
                )
                self.tokens.append(token)
            self.character_data = ""

    def __next__(self):
        size = 16 * 1024
        while self.index >= len(self.tokens) and not self.final:
            self.tokens = []
            self.index = 0
            data = self.fp.read(size)
            self.final = len(data) < size
            try:
                self.parser.Parse(data, self.final)
            except xml.parsers.expat.ExpatError as e:
                # if e.code == xml.parsers.expat.errors.XML_ERROR_NO_ELEMENTS:
                if e.code == 3:
                    pass
                else:
                    raise e
        if self.index >= len(self.tokens):
            line, column = self.pos()
            token = XmlToken(XML_EOF, None, None, line, column)
        else:
            token = self.tokens[self.index]
            self.index += 1
        return token

    def pos(self):
        return self.parser.CurrentLineNumber, self.parser.CurrentColumnNumber


class XmlTokenMismatch(Exception):
    def __init__(self, expected, found):
        self.expected = expected
        self.found = found

    def __str__(self):
        return f"{self.found.line}:{self.found.column}: {str(self.expected)} expected, {str(self.found)} found"


class XmlParser:
    """Base XML document parser."""

    def __init__(self, fp):
        self.tokenizer = XmlTokenizer(fp)
        self.consume()

    def consume(self):
        self.token = next(self.tokenizer)

    def match_element_start(self, name):
        return self.token.type == XML_ELEMENT_START and self.token.name_or_data == name

    def match_element_end(self, name):
        return self.token.type == XML_ELEMENT_END and self.token.name_or_data == name

    def element_start(self, name):
        while self.token.type == XML_CHARACTER_DATA:
            self.consume()
        if self.token.type != XML_ELEMENT_START:
            raise XmlTokenMismatch(XmlToken(XML_ELEMENT_START, name), self.token)
        if self.token.name_or_data != name:
            raise XmlTokenMismatch(XmlToken(XML_ELEMENT_START, name), self.token)
        attrs = self.token.attrs
        self.consume()
        return attrs

    def element_end(self, name):
        while self.token.type == XML_CHARACTER_DATA:
            self.consume()
        if self.token.type != XML_ELEMENT_END:
            raise XmlTokenMismatch(XmlToken(XML_ELEMENT_END, name), self.token)
        if self.token.name_or_data != name:
            raise XmlTokenMismatch(XmlToken(XML_ELEMENT_END, name), self.token)
        self.consume()

    def character_data(self, strip=True):
        data = ""
        while self.token.type == XML_CHARACTER_DATA:
            data += self.token.name_or_data
            self.consume()
        if strip:
            data = data.strip()
        return data

    def skip_element(self):
        assert self.token.type == XML_ELEMENT_START
        name = self.token.name_or_data
        self.consume()
        while self.token.type != XML_ELEMENT_END:
            if self.token.type == XML_CHARACTER_DATA:
                self.consume()
            elif self.token.type == XML_ELEMENT_START:
                self.skip_element()
            else:
                assert False
        self.element_end(name)


class JMdictParser(XmlParser):
    # http://www.csse.monash.edu.au/~jwb/jmdict_dtd_h.html

    def __init__(self, filename):
        XmlParser.__init__(self, gzip.open(filename, "rb"))

    def parse(self):
        entries = []
        self.element_start("JMdict")
        while self.token.type == XML_ELEMENT_START:
            entry = self.parse_entry()
            entries.append(entry)
            if len(entries) >= MAX_ENTRIES:
                return entries
        self.element_end("JMdict")
        entries = self.remove_orthos_for_uncommon_kanji(entries)
        return entries

    def parse_entry(self):
        kanjis = []
        readings = []
        senses = []
        orthos = []

        self.element_start("entry")
        while self.token.type == XML_ELEMENT_START:
            if self.token.name_or_data == "k_ele":
                kanji = self.parse_kanji()
                kanjis.append(kanji)
                orthos.append(Ortho(kanji.keb, kanji.rank, {}))
            elif self.token.name_or_data == "r_ele":
                reading = self.parse_reading()
                readings.append(reading)
                orthos.append(Ortho(reading.reb, reading.rank, {}))
            elif self.token.name_or_data == "sense":
                sense = self.parse_sense()
                senses.append(sense)
            else:
                self.skip_element()
        self.element_end("entry")

        # Aggregate the POS of all senses
        posses = set()
        for sense in senses:
            for pos in sense.pos:
                posses.add(pos)

        for ortho in orthos:
            # Don't try to inflect katakana words
            if not is_katakana(ortho.value):
                for pos in posses:
                    try:
                        infl_dict = inflect(ortho.value, pos)
                    except InflectionError as ex:
                        sys.stderr.write(f"error: {ex.args[0]}\n")
                    else:
                        if infl_dict:
                            ortho.inflgrps[pos] = list(infl_dict.values())

        entry = Entry(senses, orthos, kanjis, readings)

        return entry

    def parse_kanji(self):
        keb = None
        rank = sys.maxsize
        self.element_start("k_ele")
        while self.token.type == XML_ELEMENT_START:
            if self.token.name_or_data == "keb":
                keb = self.element_character_data("keb")
            elif self.token.name_or_data == "ke_pri":
                rank = min(rank, self.parse_kanji_rank())
            else:
                self.skip_element()
        self.element_end("k_ele")

        assert keb is not None
        return Kanji(keb, rank)

    def parse_reading(self):
        reb = None
        rank = 1
        re_restr = None

        self.element_start("r_ele")
        while self.token.type == XML_ELEMENT_START:
            if self.token.name_or_data == "reb":
                reb = self.element_character_data("reb")
            elif self.token.name_or_data == "re_pri":
                rank = min(rank, self.parse_reading_rank())
            elif self.token.name_or_data == "re_restr":
                re_restr = self.element_character_data("re_restr")
            else:
                self.skip_element()
        self.element_end("r_ele")
        assert reb is not None
        return Reading(reb, rank, re_restr, None)

    def parse_kanji_rank(self):
        ke_pri = self.element_character_data("ke_pri")
        if ke_pri in ("news1", "ichi1", "spec1", "gai1"):
            return 0
        else:
            return 1

    def parse_reading_rank(self):
        re_pri = self.element_character_data("re_pri")
        if re_pri in ("news1", "ichi1", "spec1", "gai1"):
            return 0
        else:
            return 1

    def parse_sense(self):
        posses = []
        dialects = []
        glosses = []
        misc_info = []
        sense_info = []
        self.element_start("sense")
        while self.token.type == XML_ELEMENT_START:
            if self.token.name_or_data == "pos":
                pos = self.element_character_data("pos")
                # revert back to entity
                pos = self.tokenizer.entities[pos]
                posses.append(pos)
            elif self.token.name_or_data == "dial":
                dial = self.element_character_data("dial")
                # revert back to entity
                dial = self.tokenizer.entities[dial]
                dialects.append(dial)
            elif self.token.name_or_data == "gloss":
                gloss = self.element_character_data("gloss")
                glosses.append(gloss)
            elif self.token.name_or_data == "misc":
                misc = self.element_character_data("misc")
                misc_info.append(misc)
            elif self.token.name_or_data == "s_inf":
                info = self.element_character_data("s_inf")
                sense_info.append(info)
            else:
                self.skip_element()
        self.element_end("sense")

        sense = Sense(posses, dialects, glosses, misc_info, sense_info)
        return sense

    def element_character_data(self, name):
        self.element_start(name)
        data = self.character_data()
        self.element_end(name)
        return data

    def remove_orthos_for_uncommon_kanji(self, entries):
        common_kanjis = []
        for entry in entries:
            for ortho in entry.orthos:
                if not is_kana(ortho[0]) and ortho[1] == 0:
                    common_kanjis.append(ortho[0])
        for entry in entries:
            entry.orthos = [
                ortho
                for ortho in entry.orthos
                if ortho[1] == 0 or not ortho[0] in common_kanjis
            ]
        return entries


class JMnedictParser(JMdictParser):
    # http://www.csse.monash.edu.au/~jwb/jmdict_dtd_h.html
    def parse(self):
        entries = []

        self.element_start("JMnedict")
        while self.token.type == XML_ELEMENT_START:
            entry = self.parse_entry()
            entries.append(entry)
            if len(entries) >= MAX_ENTRIES:
                return entries
        self.element_end("JMnedict")

        return entries

    def parse_entry(self):
        kanjis = []
        readings = []
        senses = []
        orthos = []

        self.element_start("entry")
        while self.token.type == XML_ELEMENT_START:
            if self.token.name_or_data == "k_ele":
                kanji = self.parse_kanji()
                kanjis.append(kanji)
                orthos.append(Ortho(kanji.keb, kanji.rank, {}))
            elif self.token.name_or_data == "r_ele":
                reading = self.parse_reading()
                readings.append(reading)
                orthos.append(Ortho(reading.reb, reading.rank, {}))
            elif self.token.name_or_data == "trans":
                sense = self.parse_translation()
                senses.append(sense)
            else:
                self.skip_element()
        self.element_end("entry")

        return Entry(senses, orthos, kanjis, readings, entry_type=NAME_ENTRY)

    def parse_translation(self):
        posses = []
        glosses = []
        self.element_start("trans")
        while self.token.type == XML_ELEMENT_START:
            if self.token.name_or_data == "name_type":
                pos = self.element_character_data("name_type")
                # revert back to entity
                pos = self.tokenizer.entities[pos]
                posses.append(pos)
            elif self.token.name_or_data == "trans_det":
                gloss = self.element_character_data("trans_det")
                glosses.append(gloss)
            else:
                self.skip_element()
        self.element_end("trans")

        sense = Sense(posses, [], glosses, [], [])
        return sense


def get_args():
    class DictAction(argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            if nargs is not None:
                raise ValueError("nargs not allowed")
            super().__init__(option_strings, dest, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            setattr(
                namespace,
                self.dest,
                SimpleNamespace(
                    create_jmdict="j" in values,
                    create_jmnedict="n" in values,
                    create_combined="c" in values,
                ),
            )

    arg_parser = argparse.ArgumentParser(
        description="Build the JMdict or JMnedict for Kindle",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    arg_parser.add_argument(
        "-s",
        "--sentences",
        action="store",
        default=0,
        type=int,
        metavar="count",
        help="Sets the maximum number of sentences per entry. Default is 0",
    )
    arg_parser.add_argument(
        "-d",
        "--dictionary",
        action=DictAction,
        default="j",
        type=str,
        metavar="jnc",
        help="Defines which Dictionary to create. j for JMdict, n for JMnedict, c for Combined. Default is j. You can also create multiple at the same time: -d jn for JMdict and JMnedict",
    )
    arg_parser.add_argument(
        "-p",
        "--pronunciation",
        action="store_true",
        default=False,
        help="If this flag is set pronunciations will be added to the dictionaries specified with -d",
    )
    arg_parser.add_argument(
        "-a",
        "--all_sentences",
        action="store_true",
        default=False,
        help="If this flag is set all sentences will be aded to an entry up to the number specified in --sentences. \
             If this flag is omitted only good and verified senetences will be added to the dictionaries specified with -d. If -s is 0 this argument has no effect",
    )
    arg_parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        default=False,
        help="If this flag is set additional entry information wil be added to the dictionaries specified with -d.",
    )
    return arg_parser.parse_args()


def main():
    args = get_args()

    # Create files
    if args.dictionary.create_jmdict or args.dictionary.create_combined:
        sys.stderr.write("Parsing JMdict_e.gz...\n")
        parser = JMdictParser("JMdict_e.gz")
        jmdict_entries = parser.parse()
        if args.pronunciation:
            sys.stderr.write("Adding pronunciations...\n")
            ac = Pronunciation()
            count = ac.addPronunciation(jmdict_entries)
            sys.stderr.write(f"added {count} pronunciations\n")
        sys.stderr.write(f"Created {len(jmdict_entries)} entries\n")

        if args.sentences > 0:
            sys.stderr.write("Adding sentences...\n")
            examples = ExampleSentences(
                "jpn_indices.tar.bz2", "sentences.tar.bz2", jmdict_entries
            )
            sys.stderr.write(
                f"Sentences added: {str(examples.addExamples(not args.all_sentences, args.sentences))}\n"
            )

    if args.dictionary.create_jmdict:
        sys.stderr.write("Creating files for JMdict...\n")
        write_index(
            jmdict_entries,
            "jmdict",
            "JMdict Japanese-English Dictionary",
            sys.stdout,
            default_index=VOCAB_INDEX,
            add_entry_info=args.info,
        )

    if args.dictionary.create_jmnedict or args.dictionary.create_combined:
        sys.stderr.write("Parsing JMnedict.xml.gz...\n")
        parser = JMnedictParser("JMnedict.xml.gz")
        jmnedict_entries = parser.parse()
        sys.stderr.write(f"Created {len(jmnedict_entries)} entries\n")

    if args.dictionary.create_jmnedict:
        sys.stderr.write("Creating files for JMnedict...\n")
        write_index(
            jmnedict_entries,
            "jmnedict",
            "JMnedict Japanese Names",
            sys.stdout,
            default_index=NAME_INDEX,
            add_entry_info=args.info,
        )

    if args.dictionary.create_combined:
        sys.stderr.write("Creating files for combined dictionary\n")
        write_index(
            jmdict_entries + jmnedict_entries,
            "combined",
            "JMdict Japanese-English Dictionary and JMnedict Japanese Names",
            sys.stdout,
            default_index=None,
            add_entry_info=args.info,
        )


if __name__ == "__main__":
    main()
