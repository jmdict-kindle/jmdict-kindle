import csv
from html import escape

hiragana = u'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ' \
            u'あいうえおかきくけこさしすせそたちつてと' \
            u'なにぬねのはひふへほまみむめもやゆよらりるれろ' \
            u'わをんぁぃぅぇぉゃゅょっ'
katakana = u'ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ' \
            u'アイウエオカキクケコサシスセソタチツテト' \
            u'ナニヌネノハヒフヘホマミムメモヤユヨラリルレロ' \
            u'ワヲンァィゥェォャュョッ'
hiragana = [ord(char) for char in hiragana]
translate_table = dict(zip(hiragana, katakana))

HIGH_STATE = 0
LOW_STATE = 1

class Pronunciation:

  def __init__(self):
    self.dict = {}
    with open("./pronunciation/ACCDB_unicode.csv", encoding="utf-8") as file:
      csv_reader = csv.DictReader(file, delimiter=',')
      for row in csv_reader:
        self.dict[f"{row['kanjiexpr']}-{row['midashigo']}"] = {
          'nopronouncepos':row['nopronouncepos'],
          'nasalsoundpos':row['nasalsoundpos'],
          'ac':row['ac']
        }

  def addPronunciation(self, entries):
    count = 0
    for entry in entries:
      for reading in entry.readings:
        if reading.re_restr != None:
          kanji = reading.re_restr
        elif len(entry.kanjis) > 0:
          kanji = entry.kanjis[0].keb
        else:
          kanji = ""
          
        key = f"{kanji}-{reading.reb.translate(translate_table)}"
        if key in self.dict:
          reading.pronunciation = self.dict[key]
          count += 1
        else:
          reading.pronunciation = None
    return count

def format_pronunciations(reading):
  """ Format an entry from the data in the original database to something that uses html """
  txt = reading.reb
  strlen = len(txt)
  if reading.pronunciation == None:
    return escape(txt, quote=False)
  
  acclen = len(reading.pronunciation['ac'])
  accent = "0"*(strlen-acclen) + reading.pronunciation['ac']

  # Get the nasal positions
  nasal = []
  if reading.pronunciation['nasalsoundpos']:
      positions = reading.pronunciation['nasalsoundpos'].split('0')
      for p in positions:
          if p:
              nasal.append(int(p))
          if not p:
              # e.g. "20" would result in ['2', '']
              nasal[-1] = nasal[-1] * 10

  # Get the no pronounce positions
  nopron = []
  if reading.pronunciation['nopronouncepos']:
      positions = reading.pronunciation['nopronouncepos'].split('0')
      for p in positions:
          if p:
              nopron.append(int(p))
          if not p:
              # e.g. "20" would result in ['2', '']
              nopron[-1] = nopron[-1] * 10

  outstr = ""
  if(int(accent[0]) > 0):
    state = HIGH_STATE
    outstr = outstr + '<span class="h">'
  else:
    state = LOW_STATE
    outstr = outstr + '<span class="l">'


  for i in range(strlen):
    a = int(accent[i])
    
    if(state == HIGH_STATE):
      if a == 0:
        outstr = outstr + '</span><span class="l">'
        state = LOW_STATE
    else:
      if a > 0:
        outstr = outstr + '</span><span class="h">'
        state = HIGH_STATE

    outstr = outstr + escape(txt[i], quote=False)
    if (i+1) in nopron:
      #outstr = outstr + "</span>" dont know what to do here
      outstr = outstr
    if (i+1) in nasal:
      outstr = outstr + '<span class="nas">&#176;</span>'
    if a == 2:
      outstr = outstr + '</span><span class="l">&#42780;'
      state = LOW_STATE
    
  outstr = outstr + '</span>'
  return outstr