from typing import Dict

import nltk
from nltk.corpus import brown
from random import randint


class WordFinder:
    @staticmethod
    def get_word():
        tagged_words = WordFinder.__create_tagged_word_list()
        words_and_frequencies = WordFinder.__frequency_of_words(tagged_words)
        common_word = WordFinder.__find_common_word(words_and_frequencies)
        return common_word[0], common_word[1], int(common_word[2])

    @staticmethod
    def __frequency_of_words(word_and_tags):
        word_frequencies = nltk.FreqDist((line, tag) for (line, tag) in word_and_tags)
        return word_frequencies

    @staticmethod
    def __tag_to_pos(word_tag):
        pos_dict: Dict[str, str] = {
            **dict.fromkeys(['abn', 'jj', 'jjr', 'jjs', 'jj-tl', 'jjt'], 'adjective'),
            **dict.fromkeys(['abl', 'ql', 'qlp', 'rb', 'rn', 'rp', 'rbr', 'rbt', 'wrb', 'wql'], 'adverb'),
            **dict.fromkeys(['at'], 'article'),
            **dict.fromkeys(['cc', 'cs', 'dtx'], 'conjunction'),
            **dict.fromkeys(['abx', 'ap', 'dt', 'dti', 'dts', 'dtx' 'wdt'], 'determiner'),
            **dict.fromkeys(['uh'], 'interjection'),
            **dict.fromkeys(['nn', 'nn$', 'nns', 'nns$', 'np', 'np$', 'nps$', 'nr', 'nn-tl'], 'noun'),
            **dict.fromkeys(['cd', 'od'], 'numeral'),
            **dict.fromkeys(['in'], 'preposition'),
            **dict.fromkeys(['pn', 'ex', 'pn$', 'pns$', 'pp$', 'pp$$', 'ppl', 'ppls', 'ppo', 'pps', 'ppss', 'prp',
                             'prp$', 'wp$', 'wpo', 'wps'], 'pronoun'),
            **dict.fromkeys(['vb', 'vbd', 'vbg', 'vbn', 'vbp', 'vbz', 'be', 'bed', 'bedz', 'beg', 'bem', 'ben',
                             'ber', 'bez', 'do', 'dod', 'doz', 'hvd', 'hvg', 'hvn', 'hv', 'md'], 'verb')
        }

        word_tag = word_tag.lower()
        return pos_dict.get(word_tag)

    @staticmethod
    def __find_common_word(word_and_frequencies):
        max_common = 50
        min_common = 500

        common_words = word_and_frequencies.most_common(min_common)

        index = randint(max_common, min_common)
        word = common_words[index][0][0]
        tag = common_words[index][0][1]
        return word, WordFinder.__tag_to_pos(tag), index


    @staticmethod
    def __create_tagged_word_list():
        tagged_text = brown.tagged_words()
        word_with_tag = []
        for line in tagged_text:
            word = list(line)[0]
            if word.isalpha():
                lower_line = [element.lower() for element in line]
                word_with_tag.append(lower_line)
        return word_with_tag