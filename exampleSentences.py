import tarfile
import sys
import csv
import linecache
import re

from dictionary import *

class ExampleSentences:
    
    def __init__(self, indices_tar, sentences_tar, entries):
        tarfile.open(indices_tar, "r:bz2").extractall()
        tarfile.open(sentences_tar, "r:bz2").extractall()
        csv_file = open("jpn_indices.csv", encoding="utf-8")
        self.__jpn_indices = csv.reader(csv_file, delimiter="\t")

        sentences_file = open("sentences.csv", encoding="utf-8")
        for self.sentences_count, l in enumerate(sentences_file):
            pass
        
        self.sentences_count += 1
        sentences_file.close()
        
        self.__entry_dictionary = {}
        for entry in entries:
            if(entry.entry_type == VOCAB_ENTRY):
                for ortho in entry.orthos:
                    if ortho.value in self.__entry_dictionary :
                        self.__entry_dictionary[ortho.value].append(entry)
                    else:
                        self.__entry_dictionary[ortho.value] = [entry]


    #function to find the correct sentence corresponding to the sentence id, since lines and ids do not match
    def __findSentence(self, id):
        if(id > self.sentences_count):
            current_line = self.sentences_count
        else:
            current_line = id
            
        line = linecache.getline("sentences.csv", current_line)
        columns = line.split('\t')
        columns[0] = int(columns[0])
        old_distance = abs(columns[0]-id)

        while columns[0] != id:
            assert(columns[0] >= current_line) , "there is a line with an id smaller than the line number"#this could lead to an infinite loop
            current_line = current_line - (columns[0]-id)
            line = linecache.getline("sentences.csv", current_line)
            columns = line.split('\t')
            columns[0] = int(columns[0])

            new_distance = abs(columns[0]-id)
            if(new_distance < old_distance):
                old_distance = new_distance
            else:#the entry does not exist since the numbers should converge
                return None
                
        return columns[2]

    def addExamples(self):

        added_sentences = 0

        for jpn_index in self.__jpn_indices:
            tilde_index = jpn_index[2].find('~')#only add the important sentences
            if(tilde_index != -1):

                keywords = []

                while(tilde_index != -1):
                    while(jpn_index[2][tilde_index-1] == ' '):# cut out stray spaces before ~
                        jpn_index[2] = jpn_index[2][0:(tilde_index-1)] + jpn_index[2][tilde_index:]
                        tilde_index -= 1

                    space_index = jpn_index[2].rfind(' ', 0, tilde_index)
                    keyword = jpn_index[2][(space_index + 1):tilde_index]
                    match_group = re.match('.+?(?=\W|$)', keyword)#dictionary form ends in { [ or space
                    keywords.append(match_group.group(0))
                    
                    if(tilde_index == len(jpn_index[2])-1):
                        break
                    else:
                        tilde_index = jpn_index[2].find('~', tilde_index+1)

                ja_id = int(jpn_index[0])
                eng_id = int(jpn_index[1])

                if(ja_id > 0 and eng_id > 0):

                    japanese_sentence = self.__findSentence(ja_id)
                    english_sentence = self.__findSentence(eng_id)
                
                    if(japanese_sentence != None and english_sentence != None):
                        for keyword in keywords:
                            if keyword in self.__entry_dictionary:
                                for entry in self.__entry_dictionary[keyword]:
                                    added_sentences += 1
                                    entry.sentences.append(Sentence(english_sentence, japanese_sentence))

        return added_sentences      

