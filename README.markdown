About
=====

This is a Japanese-English dictionary for Kindle Paperwhite devices based on
the [JMdict](http://www.edrdg.org/jmdict/j_jmdict.html) database.

Features:

* lookup of inflected verbs.

<!--
Screenshots were captured inside the Kindle device as explained in
http://blog.blankbaby.com/2012/10/take-a-screenshot-on-a-kindle-paperwhite.html
then processed with ImageMagick's
`mogrify -colorspace gray -level 0%,111.11% -define PNG:compression-level=9`
to look like E-Ink display.
-->

![Screenshot](screenshot.png)


Download
========

You can download the latest version of the dictionary from
[here](http://people.freedesktop.org/~jrfonseca/jmdict/).


Install
=======

To install the dictionary into your device follow these steps:

* for 1st-generation Kindle Paperwhite devices, ensure you have 
  [firmware version 5.3.9 or higher](http://www.amazon.com/gp/help/customer/display.html/ref=hp_left_cn?ie=UTF8&nodeId=201064850)
  as it includes improved homonym lookup for Japanese;

* connect your Kindle device via USB;

* copy the `jmdict.mobi` to the `documents` sub-folder;

* eject the USB device;

* on your device go to
  _Home > Settings > Device Options > Language and Dictionaries > Dictionaries_ 
  and set _JMdict Japanese-English Dictionary_ as the default dictionary for
  Japanese.


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

* Add examples from [Tanaka Corpus](http://www.edrdg.org/wiki/index.php/Tanaka_Corpus#Downloads) or [Tatoeba project](http://tatoeba.org/eng/downloads).

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

  * [Roger Häusermann's](http://www.mobileread.com/forums/showthread.php?t=223485)
