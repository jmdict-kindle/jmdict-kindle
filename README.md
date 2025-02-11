About
=====

This is a Japanese-English dictionary based on the
[JMdict](http://www.edrdg.org/jmdict/j_jmdict.html) and [JMnedict](https://www.edrdg.org/enamdict/enamdict_doc.html) and [Tatoeba](https://tatoeba.org/) database for
_e-Ink_ Kindle devices.

Features:

* lookup of inflected verbs.
* lookup for Japanese names.
* Example sentences
* Pronunciation
* the dictionaries can be downloaded as separate files or as one big dictionary

<!--
Screenshots were captured inside the Kindle device as explained in
http://blog.blankbaby.com/2012/10/take-a-screenshot-on-a-kindle-paperwhite.html
then processed with ImageMagick's
`mogrify -colorspace gray -level 0%,111.11% -define PNG:compression-level=9`
to look like E-Ink display.
-->

| ![Inflection lookup screenshot](screenshots/inflection.png) | ![Sentence lookup screenshot](screenshots/sentences.png) |
|-------------------------------------------------------------|----------------------------------------------------------|
| ![Word lookup screenshot](screenshots/word.png)             | ![Name lookup screenshot](screenshots/name.png)          |

Supported Devices
=================

The dictionary has been tested on _Kindle Paperwhite_ and _Kindle Oasis_.  It _should_ also work
well with other _e-ink_ Kindle devices

The dictionary will *not* work well on _Kindle Fire_ or _Kindle Android App_,
or any Android based Kindle, because the Kindle software on those platforms
does not support inflection lookups.


Download
========

You can download the latest version of the dictionary from
[here](https://github.com/jrfonseca/jmdict-kindle/releases).


Install
=======

_e-Ink_ Kindle
-----------------

There are in total 3 dictionaries:

* `jmdict.mobi`: Contains data from the JMedict database, with additional examples. It does not contain proper names.
* `jmnedict.mobi`: Contains Japanese proper names from the JMnedict databse.
* `combined.mobi`: Contains the data from both of the above dictionaries. _Please note that a lot of features are missing from the combined dictionary (sentences, pronunciation, ...) due to size constraints. Therefore, it is not suggested to use this dictionary_.

To install any of the dictionaries (you can also install all three of them) into your device follow these steps:

* for 1st-generation Kindle Paperwhite devices, ensure you have
  [firmware version 5.3.9 or higher](http://www.amazon.com/gp/help/customer/display.html/ref=hp_left_cn?ie=UTF8&nodeId=201064850) as it includes improved homonym lookup for Japanese;
* connect your Kindle device via USB;
* copy the the `.mobi` file for the dictionary you want to use to the `documents/dictionaries` sub-folder;
* eject the USB device;
* on your device go to
  _Home > Settings > Device Options > Language and Dictionaries > Dictionaries_
  and set _JMdict Japanese-English Dictionary_ as the default dictionary for
  Japanese.

Kindle Android App
------------------

**NOTE: Unfortunately the Kindle Android App does not support dictionary inflections, yielding verbs lookup practically impossible. No known workaround.**

* rename `jmdict.mobi` or any of the other two dictionaries as `B005FNK020_EBOK.prc`

* connect your Android device via USB

* copy `B005FNK020_EBOK.prc` into `Internal Storage/Android/data/com.amazon.kindle/files/` or `/sdcard/android/data/com.amazon.kindle/files`

This will override the
[default Japanese-Japanese dictionary](https://kindle.amazon.com/work/daijisen-x5927-x8f9e-japanese-edition-ebook/B005FNK020/B005FNK020).

Kindle iOS App
------------------

The steps for iOS App are [similar](https://learnoutlive.com/add-german-english-dictionary-to-kindle-on-your-ipad-or-iphone-ios/) the Android App above.  **Unfortunately the Kindle iOS App [seems to suffer from the same limitations regarding inflections](https://github.com/jrfonseca/jmdict-kindle/issues/15).**

Pitch accent information
====================

The pitch accent information is encoded in the following way:
* <ins>Underline</ins> for __Low__
* No Formatting for __High__
* ꜜ for a sudden __Drop__ in pitch
* ° for a __Nasal__ sound
* If no formatting whatsoever is present then we do not have pitch information for that particular entry

Examples: 
* <ins>じ</ins>たい means L-H-H
* <ins>ね</ins>が°ꜜ<ins>い</ins> means L-Hꜜ-L
* <ins>ぜ</ins>んしん means L-H-H-H
* <ins>ひ</ins>とꜜ means L-Hꜜ-(L) _[The (L) means the next sound after ひと will be low. E.g. ひとが (L-H-L)]_

For more information see [Japanese pitch accent - Wikipedia](https://en.wikipedia.org/wiki/Japanese_pitch_accent)

Building from source
====================

[![Build](https://github.com/jrfonseca/jmdict-kindle/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/jrfonseca/jmdict-kindle/actions/workflows/build.yml)

Requirements:

* Linux, Windows with Cygwin or WSL (might also work on macOS with a few changes)
* Kindle Previewer if building on Windows or WSL [Kindle Previewer](https://kdp.amazon.com/en_US/help/topic/G202131170)

  * Kindle Previewer has to be added to PATH. If normally installed add it by executing (for this change to take effect, please close all cmd and powershell windows):
  ```powershell
  Set-ItemProperty -Path 'Registry::HKEY_CURRENT_USER\Environment' -Name PATH -Value ((Get-ItemProperty -Path 'Registry::HKEY_CURRENT_USER\Environment' -Name PATH).path + ";$env:APPDATA\Amazon")
  ```

* Python version 3

  * [Pycairo](http://www.cairographics.org/pycairo)
  * [Pillow](http://pillow.readthedocs.io/en/latest/)
  * [htmlmin](https://htmlmin.readthedocs.io/en/latest/index.html)

Inside of the makefile you can change the max number of sentences per entry, compression, as well as which sentences to include:

```makefile
# The Kindle Publishing Guidelines recommend -c2 (huffdic compression),
# but it is excruciatingly slow. That's why -c1 is selected by default.
# Compression currently is not officially supported by Kindle Previewer according to the documentation
COMPRESSION ?= 1

# Sets the max sentences per entry only for the jmdict.mobi.
# It is ignored by combined.mobi due to size restrictions.
# If there are too many sentences for the combined dictionary,
# it will not build (exceeds 650MB size limit). The amount is limited to 0 in this makefile for the combined.mobi
SENTENCES ?= 5

# This flag determines wheter only good and verified sentences are used in the
# dictionary. Set it to TRUE if you only want those sentences.
# It is only used by jmdict.mobi
# It is ignored bei combined.mobi. There it is always true
# This is due to size constraints.
ONLY_CHECKED_SENTENCES ?= FALSE

# If true adds pronunciations to entries. The combined dictionary ignores this flag due to size constraints
PRONUNCIATIONS ?= TRUE

# If true adds additional information to entries. The combined dictionary ignores this flag due to size constraints
ADDITIONAL_INFO ?= TRUE
```

Build with make to create all 3 dictionaries (_Note the combined dictionary will not build with Kindle Previewer due to size constraints_):
```
make
```
or use any of the following commands to create a specific one:
```
make jmdict.mobi
make jmnedict.mobi
make combined.mobi
```

If you build it on WSL the commands are as follows:
```
make ISWSL=TRUE
```
or use any of the following commands to create a specific one:
```
make jmdict.mobi ISWSL=TRUE
make jmnedict.mobi ISWSL=TRUE
make combined.mobi ISWSL=TRUE
```

Create a Pull Request
=====
Before making a pull request please ensure the formatting of your python code is correct. To do this please install [black](https://pypi.org/project/black/) and run

```powershell
black .
```

To do
=====

* Leverage more of the JMdict data:

  * cross references
* Add Furigana to example sentences
* Create better covers


Credits
=======

* Jim Breen and the [JMdict/EDICT project](http://www.edrdg.org/jmdict/j_jmdict.html) as well as the [ENAMDICT/JMnedict](https://www.edrdg.org/enamdict/enamdict_doc.html)
* The [Tatoeba](https://tatoeba.org/) project
* John Mettraux for his [EDICT2 Japanese-English Kindle dictionary](https://github.com/jmettraux/edict2-kindle)
* Choplair-network for their [Nihongo conjugator](http://www.choplair.org/?Nihongo%20conjugator)
* javdejong for the [pronunciation data and the parser](https://github.com/javdejong/nhk-pronunciation)
* mifunetoshiro for the [additional pronunciation data](https://github.com/mifunetoshiro/kanjium/blob/main/data/source_files/raw/accents.txt)


Alternatives
============

* [John Mettraux's EDICT2 Japanese-English Kindle dictionary](https://github.com/jmettraux/edict2-kindle)

* [Amazon Kindle Store](http://www.amazon.com/s/url=search-alias%3Ddigital-text&field-keywords=japanese+english+dictionary)
