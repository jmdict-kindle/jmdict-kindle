PYTHON ?= python

default: jmdict.mobi

JMdict_e.gz:
	wget -nv -N http://ftp.monash.edu.au/pub/nihongo/$@

KINDLEGEN_PKG ?= kindlegen_linux_2.6_i386_v2_9.tar.gz

$(KINDLEGEN_PKG):
	wget -nv -N https://kindlegen.s3.amazonaws.com/$@

kindlegen: $(KINDLEGEN_PKG)
	tar -xzf $(KINDLEGEN_PKG) kindlegen
	touch $@

jmdict.opf: jmdict.py dictionary.py inflections.py kana.py JMdict_e.gz
	$(PYTHON) jmdict.py

cover.jpg: cover.py
	$(PYTHON) cover.py

# XXX: The Kindle Publishing Guidelines recommend -c2 (huffdic compression),
# but it is excruciatingly slow.
COMPRESSION ?= 1

# See also https://wiki.mobileread.com/wiki/KindleGen
jmdict.mobi: jmdict.opf cover.jpg style.css frontmatter.html kindlegen
	./kindlegen $< -c$(COMPRESSION) -verbose -dont_append_source -o $@

clean:
	rm -f *.mobi *.opf entry-*.html cover.jpg

.PHONE: default clean
