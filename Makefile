PYTHON3 ?= python3

default: jmdict.mobi

JMdict_e.gz:
	wget -nv -N http://ftp.monash.edu.au/pub/nihongo/$@
	
sentences.tar.bz2:
	wget -nv -N http://downloads.tatoeba.org/exports/$@
	
jpn_indices.tar.bz2:
	wget -nv -N http://downloads.tatoeba.org/exports/$@

KINDLEGEN_PKG ?= kindlegen_linux_2.6_i386_v2_9.tar.gz

$(KINDLEGEN_PKG):
	wget -nv -N https://kindlegen.s3.amazonaws.com/$@

kindlegen: $(KINDLEGEN_PKG)
	tar -xzf $(KINDLEGEN_PKG) kindlegen
	touch $@

jmdict.opf: jmdict.py dictionary.py inflections.py kana.py JMdict_e.gz sentences.tar.bz2 jpn_indices.tar.bz2
	$(PYTHON3) jmdict.py

cover.jpg: cover.py
	$(PYTHON3) cover.py

# XXX: The Kindle Publishing Guidelines recommend -c2 (huffdic compression),
# but it is excruciatingly slow.
COMPRESSION ?= 1

# See also https://wiki.mobileread.com/wiki/KindleGen
jmdict.mobi: jmdict.opf cover.jpg style.css frontmatter.html kindlegen
	./kindlegen $< -c$(COMPRESSION) -verbose -dont_append_source -o $@

clean:
	rm -f *.mobi *.opf entry-*.html cover.jpg *.tar.bz2 *.gz *.csv cover.png

.PHONE: default clean
