#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on https://tproger.ru/translations/markov-chains/

import os
import utils
from datatypes.markov import MarkovModel


class StatisticData:
    num_of_parsed_files = 0
    num_of_parsed_lines = 0
    num_of_parsed_sentences = 0
    num_of_parsed_words = 0

    @staticmethod
    def inc_parsed_files():
        StatisticData.num_of_parsed_files += 1

    @staticmethod
    def inc_parsed_lines(n):
        StatisticData.num_of_parsed_lines += n

    @staticmethod
    def inc_parsed_sentences(n):
        StatisticData.num_of_parsed_sentences += n

    @staticmethod
    def inc_parsed_words(n):
        StatisticData.num_of_parsed_words += n


markov_data = MarkovModel()


def parse(source):
    StatisticData.inc_parsed_files()
    with open(source, 'r') as s:
        lines = s.readlines()
    StatisticData.inc_parsed_lines(len(lines))

    flatten_lines = []
    for line in lines:
        flatten_lines += line
    flatten_lines = ''.join(flatten_lines).replace('\n', ' ')
    sentences = list(map(utils.format_sentence, filter(utils.not_empty, flatten_lines.split('.'))))

    StatisticData.inc_parsed_sentences(len(sentences))

    for sentence in sentences:
        splitted_sentence = list(map(utils.format_word, filter(utils.not_empty, sentence.split(' '))))
        StatisticData.inc_parsed_words(len(splitted_sentence))
        markov_data.update_model(splitted_sentence)


if __name__ == "__main__":
    for s in [os.path.join(os.getcwd(), "source", x) for x in os.listdir("source") if
              (not x.endswith('.py'))]:
        parse(s)

    print("Total parsed files: %d" % StatisticData.num_of_parsed_files)
    print("Total parsed lines: %d" % StatisticData.num_of_parsed_lines)
    print("Total parsed sentences: %d" % StatisticData.num_of_parsed_sentences)
    print("Total parsed words: %d" % StatisticData.num_of_parsed_words)

    print("Try to generate sentence by max weight:")

    length = 20
    current_key = markov_data.get_random_start()
    new_sentence = [current_key[1]]
    while utils.end_token not in current_key and length > 0:
        if markov_data[current_key]:
            new_word = markov_data[current_key].return_weighted_random_word()
        else:
            new_sentence.append('; ')
            new_word = markov_data.get_random_start()

        new_sentence.append(new_word)
        current_key = (current_key[1], new_word)
        length -= 1

    if utils.end_token in new_sentence:
        new_sentence.remove(utils.end_token)

    new_sentence[0] = new_sentence[0].capitalize()
    print(' '.join(new_sentence) + '.')
