# XXX: The Kindle Publishing Guidelines recommend -c2 (huffdic compression),
# but it is excruciatingly slow.
COMPRESSION ?= 1
#if this number is too high the combined dictionary will be too large and not compile
SENTENCES ?= 5
# only add sentences that are marked
ONLY_CHECKED_SENTENCES ?= FALSE

ifeq ($(OS), Windows_NT)
	PYTHON3 ?= python
	KINDLEGEN_PKG ?= kindlegen_win32_v2_9.zip
	KINDLEGEN ?= kindlegen.exe
else
	PYTHON3 ?= python3
	KINDLEGEN_PKG ?= kindlegen_linux_2.6_i386_v2_9.tar.gz
	KINDLEGEN ?= kindlegen
endif

all: jmdict.mobi jmnedict.mobi combined.mobi

JMdict_e.gz:
	wget -nv -N http://ftp.monash.edu.au/pub/nihongo/$@
	
JMnedict.xml.gz:
	wget -nv -N http://ftp.monash.edu/pub/nihongo/$@
	
sentences.tar.bz2:
	wget -nv -N http://downloads.tatoeba.org/exports/$@
	
jpn_indices.tar.bz2:
	wget -nv -N http://downloads.tatoeba.org/exports/$@
	
kindlegen:
	wget -nv -N https://kindlegen.s3.amazonaws.com/$(KINDLEGEN_PKG)
ifeq ($(OS), Windows_NT)
	unzip -o $(KINDLEGEN_PKG) kindlegen.exe
	touch kindlegen.exe
	chmod 700 kindlegen.exe
else
	tar -xzf $(KINDLEGEN_PKG) kindlegen
	touch kindlegen
endif

JMdict.opf JMnedict.opf JMdict_and_JMnedict.opf: jmdict.py dictionary.py inflections.py kana.py JMdict_e.gz JMnedict.xml.gz sentences.tar.bz2 jpn_indices.tar.bz2
ifeq ($(ONLY_CHECKED_SENTENCES), TRUE)
	$(PYTHON3) jmdict.py -s $(SENTENCES) -d jnc
else
	$(PYTHON3) jmdict.py -a -s $(SENTENCES) -d jnc
endif

# See also https://wiki.mobileread.com/wiki/KindleGen
jmdict.mobi: JMdict.opf style.css JMdict-frontmatter.html kindlegen
	./$(KINDLEGEN) $< -c$(COMPRESSION) -verbose -dont_append_source -o $@
	
jmnedict.mobi: JMnedict.opf style.css JMnedict-frontmatter.html kindlegen
	./$(KINDLEGEN) $< -c$(COMPRESSION) -verbose -dont_append_source -o $@
	
combined.mobi: JMdict_and_JMnedict.opf style.css JMdict_and_JMnedict-Frontmatter.html kindlegen
	./$(KINDLEGEN) $< -c$(COMPRESSION) -verbose -dont_append_source -o $@	

clean:
	rm -f *.mobi *.opf entry-*.html *cover.jpg *.tar.bz2 *.gz *.csv *cover.png kindlegen *.tmp *.zip kindlegen.exe	
	
.PHONY: all clean
