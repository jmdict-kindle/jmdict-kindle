About
=====

This is a Japanese-English dictionary for Kindle based on the JMdict database.

Features:

* on ambiguity, precedence is given to most common entries

* inflection of verbs


Building from source
====================

Requirements:

* Python version 2.7

  * Python Cairo

  * Python Image Library

* [kindlegen 2.8](http://s3.amazonaws.com/kindlegen/kindlegen_linux_2.6_i386_v2_8.tar.gz) (2.9 crashes for me)


Build with:

    make


To do
=====


* Leverage more of the JMdict data:

  * cross references

  * more accurate word frequency modelling

* More effective inflections.

* Include a subset of Japanese proper names from [ENAMDICT/JMnedict](http://www.csse.monash.edu.au/~jwb/enamdict_doc.html).


Credits
=======

* Jim Breen and the [JMdict/EDICT project](http://www.edrdg.org/jmdict/j_jmdict.html)

* John Mettraux for his [EDICT2 Japanese-English Kindle dictionary](https://github.com/jmettraux/edict2-kindle)

* Choplair-network for their [Nihongo conjugator](http://www.choplair.org/?Nihongo%20conjugator)
