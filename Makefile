PYTHON3 ?= python3

all: jmdict.mobi jmnedict.mobi

JMdict_e.gz:
	wget -nv -N http://ftp.monash.edu.au/pub/nihongo/$@
	
JMnedict.xml.gz:
	wget -nv -N http://ftp.monash.edu/pub/nihongo/$@
	
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

JMdict.opf JMnedict.opf: jmdict.py dictionary.py inflections.py kana.py JMdict_e.gz JMnedict.xml.gz sentences.tar.bz2 jpn_indices.tar.bz2
	$(PYTHON3) jmdict.py

JMdict-cover.jpg JMnedict-cover.jpg: cover.py
	$(PYTHON3) cover.py

# XXX: The Kindle Publishing Guidelines recommend -c2 (huffdic compression),
# but it is excruciatingly slow.
COMPRESSION ?= 1

# See also https://wiki.mobileread.com/wiki/KindleGen
jmdict.mobi: JMdict.opf JMdict-cover.jpg style.css JMdict-frontmatter.html kindlegen
	./kindlegen $< -c$(COMPRESSION) -verbose -dont_append_source -o $@
	
jmnedict.mobi: JMnedict.opf JMnedict-cover.jpg style.css JMnedict-frontmatter.html kindlegen
	./kindlegen $< -c$(COMPRESSION) -verbose -dont_append_source -o $@

clean:
	rm -f *.mobi *.opf entry-*.html *cover.jpg *.tar.bz2 *.gz *.csv *cover.png kindlegen

.PHONE: default clean
