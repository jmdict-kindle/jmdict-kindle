About
=====

This is a Japanese-English dictionary for Kindle Paperwhite based on the JMdict database.

Features:

* on ambiguity, precedence is given to most common entries

* inflection of verbs


Download
========

You can download the latest version from [here](http://people.freedesktop.org/~jrfonseca/jmdict/).


Building from source
====================

Requirements:

* Unix (tested with Linux but might work on MacOS or Cygwin with little or no changes)

* Python version 2.7

  * [Pycairo Python](http://www.cairographics.org/pycairo)

  * [Python Image Library](http://www.pythonware.com/products/pil/)

* [kindlegen 2.8](http://s3.amazonaws.com/kindlegen/kindlegen_linux_2.6_i386_v2_8.tar.gz) (2.9 crashes for me)


Build with:

    make


To do
=====

* Leverage more of the JMdict data:

  * cross references

  * more accurate word frequency modelling

* Merge ambiguous entries (as opposed to remove the less frequent ones)

* More effective inflections.

* Add examples from [Tanaka Corpus](http://www.edrdg.org/wiki/index.php/Tanaka_Corpus#Downloads) or [Tatoeba project](http://tatoeba.org/eng/downloads)

* Include a subset of Japanese proper names from [ENAMDICT/JMnedict](http://www.csse.monash.edu.au/~jwb/enamdict_doc.html).


Credits
=======

* Jim Breen and the [JMdict/EDICT project](http://www.edrdg.org/jmdict/j_jmdict.html)

* John Mettraux for his [EDICT2 Japanese-English Kindle dictionary](https://github.com/jmettraux/edict2-kindle)

* Choplair-network for their [Nihongo conjugator](http://www.choplair.org/?Nihongo%20conjugator)


Alternatives
============

* [John Mettraux's EDICT2 Japanese-English Kindle dictionary](https://github.com/jmettraux/edict2-kindle)

* [Amazon Kindle Store](http://www.amazon.com/gp/bestsellers/digital-text/158211011/)
