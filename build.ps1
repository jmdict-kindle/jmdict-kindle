$SENTENCES = 5
$ONLY_CHECKED_SENTENCES = $false
$PRONUNCIATIONS = $true
$ADDITIONAL_INFO = $true

$FLAGS = ""
if(!$ONLY_CHECKED_SENTENCES)
{
    $FLAGS += " -a"
}
if($PRONUNCIATIONS)
{
    $FLAGS += " -p"
}
if($ADDITIONAL_INFO)
{
    $FLAGS += " -i"
}

Write-Output "downloading data"
Invoke-WebRequest -Uri "http://ftp.edrdg.org/pub/Nihongo/JMdict_e.gz" -OutFile ".\JMdict_e.gz"
Invoke-WebRequest -Uri "http://ftp.edrdg.org/pub/Nihongo/JMnedict.xml.gz" -OutFile ".\JMnedict.xml.gz"
Invoke-WebRequest -Uri "https://downloads.tatoeba.org/exports/sentences.tar.bz2" -OutFile ".\sentences.tar.bz2"
Invoke-WebRequest -Uri "https://downloads.tatoeba.org/exports/jpn_indices.tar.bz2" -OutFile ".\jpn_indices.tar.bz2"

Write-Output "create files for JMdict"
& "python" -u jmdict.py -s $SENTENCES -d j $FLAGS.Split(" ")
Write-Output "create files for JMnedict"
& "python" -u jmdict.py -s $SENTENCES -d n $FLAGS.Split(" ")
Write-Output "create files for combined dictionary"
& "python" -u jmdict.py -s 0 -d c

If (!(test-path .\out))
{
    md .\out
}

Write-Output "building jmdict.mobi"
& "$($env:APPDATA)\Amazon\kindlepreviewer.bat" "jmdict.opf" -convert -output .\out -locale en
cp .\out\mobi\jmdict.mobi .\jmdict.mobi
Write-Output "building jmnedict.mobi"
& "$($env:APPDATA)\Amazon\kindlepreviewer.bat" "jmnedict.opf" -convert -output .\out -locale en
cp .\out\mobi\jmnedict.mobi .\jmnedict.mobi
Write-Output "building combined.mobi"
& "$($env:APPDATA)\Amazon\kindlepreviewer.bat" "combined.opf" -convert -output .\out -locale en
cp .\out\mobi\combined.mobi .\combined.mobi