# The Kindle Publishing Guidelines recommend -c2 (huffdic compression),
# but it is excruciatingly slow. That's why -c1 is selected by default.
COMPRESSION ?= 1
# Sets the max sentences per entry only for the jmdict.mobi.
# It is ignored by combined.mobi due to size restrictions.
# If there are too many sentences for the combined dictionary,
# it will not build (exceeds 650MB size limit).
SENTENCES ?= 5
# This flag determines wheter only good and verified sentences are used in the
# dictionary. Set it to TRUE if you only want those sentences.
# It is only used by jmdict.mobi
# It is ignored bei combined.mobi. there it is always true
# this is due to size constraints.
ONLY_CHECKED_SENTENCES ?= FALSE

PRONUNCIATIONS ?= TRUE

ifeq ($(PRONUNCIATIONS), TRUE)
	PRONUNCIATIONS_FLAG ?= -p
endif

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

# See also https://wiki.mobileread.com/wiki/KindleGen
jmdict.mobi: JMdict_e.gz sentences.tar.bz2 jpn_indices.tar.bz2 style.css JMdict-frontmatter.html kindlegen
ifeq ($(ONLY_CHECKED_SENTENCES), TRUE)
	$(PYTHON3) jmdict.py -s $(SENTENCES) -d j $(PRONUNCIATIONS_FLAG)
else
	$(PYTHON3) jmdict.py -a -s $(SENTENCES) -d j $(PRONUNCIATIONS_FLAG)
endif

	
jmnedict.mobi: JMnedict.xml.gz style.css JMnedict-Frontmatter.html kindlegen
	$(PYTHON3) jmdict.py -d n
	

#Currently the limit for sentences is around 30000. After that the file becomes too big	
combined.mobi: JMdict_e.gz JMnedict.xml.gz sentences.tar.bz2 jpn_indices.tar.bz2 style.css JMdict_and_JMnedict-Frontmatter.html kindlegen
	$(PYTHON3) jmdict.py -s 0 -d c $(PRONUNCIATIONS_FLAG)


clean:
	rm -f *.mobi *.opf entry-*.html *cover.jpg *.tar.bz2 *.gz *.csv *cover.png kindlegen *.tmp *.zip kindlegen.exe	
	
.PHONY: all
