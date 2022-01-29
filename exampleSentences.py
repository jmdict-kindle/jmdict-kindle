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
            if entry.entry_type == VOCAB_ENTRY:
                for ortho in entry.orthos:
                    if ortho.value in self.__entry_dictionary:
                        self.__entry_dictionary[ortho.value].append(entry)
                    else:
                        self.__entry_dictionary[ortho.value] = [entry]

    # function to find the correct sentence corresponding to the sentence id, since lines and ids do not match
    def __findSentence(self, id):
        if id > self.sentences_count:
            current_line = self.sentences_count
        else:
            current_line = id

        line = linecache.getline("sentences.csv", current_line)
        columns = line.split("\t")
        columns[0] = int(columns[0])
        old_distance = abs(columns[0] - id)

        while columns[0] != id:
            assert columns[0] >= current_line, "The sentence list is not ordered"
            current_line = current_line - (columns[0] - id)
            line = linecache.getline("sentences.csv", current_line)
            columns = line.split("\t")
            columns[0] = int(columns[0])

            new_distance = abs(columns[0] - id)
            if new_distance < old_distance:
                old_distance = new_distance
            else:  # if it is stuck try linear search from that point on
                if columns[0] > id:
                    while columns[0] > id:
                        current_line -= 1
                        line = linecache.getline("sentences.csv", current_line)
                        columns = line.split("\t")
                        columns[0] = int(columns[0])
                elif columns[0] < id:
                    while columns[0] < id:
                        current_line += 1
                        line = linecache.getline("sentences.csv", current_line)
                        columns = line.split("\t")
                        columns[0] = int(columns[0])
                break
        if columns[0] == id:
            # remove linebreak
            columns[2] = columns[2].replace("\n", "")
            return columns[2]
        else:
            return None

    def addExamples(self, good_only, max_sentences):

        added_sentences = 0

        for jpn_index in self.__jpn_indices:

            keywords = []

            if good_only:
                sections = jpn_index[2].split("~")  # good keywords are marked with an ~
                del sections[-1]  # remove the last section since it did not contain a ~

                for section in sections:
                    split = section.split(" ")
                    keyword = split[-1]
                    match_group = re.match(".+?(?=\W|$|~)", keyword)
                    if match_group:
                        keywords.append([match_group.group(0), True])
            else:
                for keyword in jpn_index[2].split(" "):
                    if len(keyword) > 0:
                        if keyword[-1] == "~":  # good keywords are marked with an ~
                            good_keyword = True
                        else:
                            good_keyword = False
                        # only take the word after the word there can be ()[]{}~|
                        match_group = re.match(".+?(?=\W|$|~)", keyword)
                        if match_group:
                            keywords.append([match_group.group(0), good_keyword])

            if len(keywords) > 0:
                ja_id = int(jpn_index[0])
                eng_id = int(jpn_index[1])

                if ja_id > 0 and eng_id > 0:

                    japanese_sentence = self.__findSentence(ja_id)
                    english_sentence = self.__findSentence(eng_id)

                    if japanese_sentence != None and english_sentence != None:
                        for keyword in keywords:
                            if keyword[0] in self.__entry_dictionary:
                                for entry in self.__entry_dictionary[keyword[0]]:
                                    if len(entry.sentences) < max_sentences:
                                        added_sentences += 1
                                        entry.sentences.append(
                                            Sentence(
                                                english_sentence,
                                                japanese_sentence,
                                                keyword[1],
                                            )
                                        )
                                    elif keyword[1] == True:
                                        for i in range(len(entry.sentences)):
                                            if not entry.sentences[i].good_sentence:
                                                entry.sentences[i] = Sentence(
                                                    english_sentence,
                                                    japanese_sentence,
                                                    keyword[1],
                                                )
                                                break

        return added_sentences
