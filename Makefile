# The Kindle Publishing Guidelines recommend -c2 (huffdic compression),
# but it is excruciatingly slow. That's why -c1 is selected by default.
COMPRESSION ?= 1

# Sets the max sentences per entry only for the jmdict.mobi.
# It is ignored by combined.mobi due to size restrictions.
# If there are too many sentences for the combined dictionary,
# it will not build (exceeds 650MB size limit). The amount is limited to 3 in this makefile
SENTENCES ?= 5

# This flag determines wheter only good and verified sentences are used in the
# dictionary. Set it to TRUE if you only want those sentences.
# It is only used by jmdict.mobi
# It is ignored bei combined.mobi. there it is always true
# this is due to size constraints.
ONLY_CHECKED_SENTENCES ?= FALSE

# If true adds pronunciations indication
PRONUNCIATIONS ?= TRUE

ifeq ($(PRONUNCIATIONS), TRUE)
	PRONUNCIATIONS_FLAG ?= -p
endif

ifeq ($(OS), Windows_NT)
	PYTHON3 ?= python
	KINDLEGEN ?= kindlegen.exe
	$(error FIXME: Use kindlegen included in Kindle Previewer)
else
	PYTHON3 ?= python3
	KINDLEGEN ?= ./kindlegen
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

ifneq ($(OS), Windows_NT)

cache:
	mkdir $@

cache/kindlegen_linux_2.6_i386_v2_9.tar.gz: cache
	wget -nv -O $@ https://www.dropbox.com/s/dl/vvg1n3mu04fdkoh

kindlegen: cache/kindlegen_linux_2.6_i386_v2_9.tar.gz
	tar -xzf $< $@
	touch $@
endif

# See also https://wiki.mobileread.com/wiki/KindleGen
jmdict.mobi: JMdict_e.gz sentences.tar.bz2 jpn_indices.tar.bz2 style.css JMdict-frontmatter.html $(KINDLEGEN)
ifeq ($(ONLY_CHECKED_SENTENCES), TRUE)
	$(PYTHON3) jmdict.py -s $(SENTENCES) -d j $(PRONUNCIATIONS_FLAG)
else
	$(PYTHON3) jmdict.py -a -s $(SENTENCES) -d j $(PRONUNCIATIONS_FLAG)
endif
	$(KINDLEGEN) JMdict.opf -c$(COMPRESSION) -verbose -dont_append_source -o $@

jmnedict.mobi: JMnedict.xml.gz style.css JMnedict-Frontmatter.html $(KINDLEGEN)
	$(PYTHON3) jmdict.py -d n
	$(KINDLEGEN) JMnedict.opf -c$(COMPRESSION) -verbose -dont_append_source -o $@

#Currently the limit for sentences is around 30000. After that the file becomes too big
combined.mobi: JMdict_e.gz JMnedict.xml.gz sentences.tar.bz2 jpn_indices.tar.bz2 style.css JMdict_and_JMnedict-Frontmatter.html $(KINDLEGEN)
	if [ $(SENTENCES) -gt 3 ]; then \
		$(PYTHON3) jmdict.py -s 3 -d c ; \
	else  \
		$(PYTHON3) jmdict.py -s $(SENTENCES) -d c ; \
	fi
	$(KINDLEGEN) JMdict_and_JMnedict.opf -c$(COMPRESSION) -verbose -dont_append_source -o $@

clean:
	rm -f *.mobi *.opf entry-*.html *cover.jpg *.tar.bz2 *.gz *.csv *cover.png *.tmp *.zip

.PHONY: all clean
