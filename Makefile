PYTHON3 ?= python

all: jmdict.mobi jmnedict.mobi combined.mobi

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

JMdict.opf JMnedict.opf JMdict_and_JMnedict.opf: jmdict.py dictionary.py inflections.py kana.py JMdict_e.gz JMnedict.xml.gz sentences.tar.bz2 jpn_indices.tar.bz2
	$(PYTHON3) jmdict.py

# XXX: The Kindle Publishing Guidelines recommend -c2 (huffdic compression),
# but it is excruciatingly slow.
COMPRESSION ?= 2

# See also https://wiki.mobileread.com/wiki/KindleGen
jmdict.mobi: JMdict.opf style.css JMdict-frontmatter.html kindlegen
	kindlegen $< -c$(COMPRESSION) -verbose -dont_append_source -o $@
	
jmnedict.mobi: JMnedict.opf style.css JMnedict-frontmatter.html kindlegen
	kindlegen $< -c$(COMPRESSION) -verbose -dont_append_source -o $@
	
combined.mobi: JMdict_and_JMnedict.opf style.css JMdict_and_JMnedict-Frontmatter.html kindlegen
	kindlegen $< -c$(COMPRESSION) -verbose -dont_append_source -o $@	

clean:
	rm -f *.mobi *.opf entry-*.html *cover.jpg *.tar.bz2 *.gz *.csv *cover.png kindlegen

.PHONE: default clean
