default: jmdict.mobi

edict2.gz enamdict.gz JMdict_e.gz JMnedict.xml.gz:
	wget -N http://ftp.monash.edu.au/pub/nihongo/$@

%.txt: %.gz edict_to_txt.py
	python edict_to_txt.py $< > $@

#definitions.html: edict2_to_html.py dictionary.py edict2.gz
#	python edict2_to_html.py > $@

definitions.html: jmdict.py dictionary.py inflections.py JMdict_e.gz
	python jmdict.py > $@

cover.jpg: cover.py
	python cover.py

# XXX: The Kindle Publishing Guidelines recommend -c2 (huffdic compression),
# but it is excruciantly slow.
COMPRESSION ?= 1

jmdict.mobi: jmdict.opf cover.jpg style.css frontmatter.html definitions.html
	kindlegen $< -c$(COMPRESSION) -verbose -o $@

publish: jmdict.mobi
	scp -p jmdict.mobi annarchy.freedesktop.org:public_html/jmdict/
