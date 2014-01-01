default: jmdict.mobi

edict2.gz enamdict.gz JMdict_e.gz JMnedict.xml.gz:
	wget -N http://ftp.monash.edu.au/pub/nihongo/$@.gz

%.txt: %.gz edict_to_txt.py
	python edict_to_txt.py $< > $@

#definitions.html: edict2_to_html.py dictionary.py edict2.gz
#	python edict2_to_html.py > $@

definitions.html: jmdict.py dictionary.py inflections.py JMdict_e.gz
	python jmdict.py > $@

cover.jpg: cover.py
	python cover.py

# http://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211
# XXX: Should be -c2 but it is very slow
jmdict.mobi: jmdict.opf cover.jpg style.css frontmatter.html definitions.html
	kindlegen jmdict.opf -c1 -verbose
