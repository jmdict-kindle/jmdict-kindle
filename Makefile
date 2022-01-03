# The Kindle Publishing Guidelines recommend -c2 (huffdic compression),
# but it is excruciatingly slow. That's why -c1 is selected by default.
# Compression currently is not officially supported by Kindle Previewer according to the documentation
COMPRESSION ?= 1

# Sets the max sentences per entry
# If there are too many sentences for the combined dictionary,
# it will not build (exceeds 650MB size limit). The amount is limited to 0 in this makefile for the combined.mobi
SENTENCES ?= 5

# This flag determines wheter only good and verified sentences are used in the
# dictionary. Set it to TRUE if you only want those sentences.
# It is only used by jmdict.mobi
# It is ignored bei combined.mobi. There it is always true
# This is due to size constraints.
ONLY_CHECKED_SENTENCES ?= FALSE

# If true adds pronunciations indication
PRONUNCIATIONS ?= TRUE

ifeq ($(PRONUNCIATIONS), TRUE)
	PRONUNCIATIONS_FLAG ?= -p
endif

ifeq ($(OS), Windows_NT)
	PYTHON3 ?= python
	KINDLEGEN ?= kindlepreviewer.bat
else
	PYTHON3 ?= python3
	KINDLEGEN ?= ./kindlegen
endif

all: jmdict.mobi jmnedict.mobi combined.mobi

JMdict_e.gz:
	wget -nv -N http://ftp.edrdg.org/pub/Nihongo/$@

JMnedict.xml.gz:
	wget -nv -N http://ftp.edrdg.org/pub/Nihongo/$@

sentences.tar.bz2:
	wget -nv -N https://downloads.tatoeba.org/exports/$@

jpn_indices.tar.bz2:
	wget -nv -N https://downloads.tatoeba.org/exports/$@

ifeq ($(OS), Windows_NT)
# See also http://kindlepreviewer3.s3.amazonaws.com/UserGuide320_EN.pdf
kindlegen:
	if ! command -v $(KINDLEGEN) &> /dev/null \
	then \
		$error("Please install Kindle Previewer before executing this script and make sure C:/Users/<Username>/AppData/Roaming/Amazon is added to PATH") \
	fi
else
cache:
	mkdir $@
	
# Note that kindlegen was officially replaced by Kindle Previewer
cache/kindlegen_linux_2.6_i386_v2_9.tar.gz: cache
	wget -nv -O $@ https://www.dropbox.com/s/dl/vvg1n3mu04fdkoh

# See also https://wiki.mobileread.com/wiki/KindleGen
kindlegen: cache/kindlegen_linux_2.6_i386_v2_9.tar.gz
	tar -xzf $< $@
	touch $@
endif

jmdict.opf: JMdict_e.gz sentences.tar.bz2 jpn_indices.tar.bz2 style.css JMdict-frontmatter.html
ifeq ($(ONLY_CHECKED_SENTENCES), TRUE)
	$(PYTHON3) jmdict.py -s $(SENTENCES) -d j $(PRONUNCIATIONS_FLAG)
else
	$(PYTHON3) jmdict.py -a -s $(SENTENCES) -d j $(PRONUNCIATIONS_FLAG)
endif

jmnedict.opf: JMnedict.xml.gz style.css JMnedict-Frontmatter.html
	$(PYTHON3) jmdict.py -d n

combined.opf: JMdict_e.gz JMnedict.xml.gz sentences.tar.bz2 jpn_indices.tar.bz2 style.css Combined-Frontmatter.html
#Currently the combined dictionary wont build with sentences on windows with Kindle Previewer due to size constraints
	if [ $(SENTENCES) -gt 0 ]; then \
		$(PYTHON3) jmdict.py -s 0 -d c ; \
	else  \
		$(PYTHON3) jmdict.py -s $(SENTENCES) -d c ; \
	fi

%.mobi: %.opf kindlegen 
ifeq ($(OS), Windows_NT)
	mkdir -p out
	$(KINDLEGEN) $< -convert -output ./out -locale en
	cp ./out/mobi/$@ ./$@
else
	$(KINDLEGEN) $< -c$(COMPRESSION) -verbose -dont_append_source -o $@
endif

clean:
	rm -rf *.opf entry-*.html *cover.jpg *.tar.bz2 *.gz *.csv *cover.png *.tmp *.zip out cache

clean_all: clean
	rm -rf *.mobi

.PHONY: all clean
