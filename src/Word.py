from random import randint
from typing import Dict

import nltk
from nltk import text
from nltk.corpus import wordnet as wn
import pronouncing


class Word:
    def __init__(self, word, pos, frequency):
        is_synset_missing = True

        while is_synset_missing:
            self.synset = wn.synsets(word)

            if self.synset:
                self.synset = self.synset[0]
                self.lemma = self.__syn_to_string(self.synset)[0]
                self.pos = pos
                self.frequency = frequency

                is_synset_missing = False

    def print(self):
        print(self.lemma)

    def length(self):
        return len(self.lemma)

    def contains_letter(self, letter):
        return letter.lower() in self.lemma

    def is_nth_letter(self, letter, index):
        return letter.lower() == self.lemma[index]

    def nth_letter(self, index):
        if index < self.length():
            return self.lemma[index]
        else:
            return "?"

    def first_letter(self):
        return self.nth_letter(0)

    def second_letter(self):
        return self.nth_letter(1)

    def last_letter(self):
        return self.nth_letter(-1)

    def find_similar_words(self):
        text_context_index = nltk.text.ContextIndex([w.lower() for w in nltk.corpus.brown.words()])
        similar = text_context_index.similar_words(self.lemma, 10)
        similar_words = ', '.join(similar)
        return similar_words

    def get_pos(self):
        return self.pos

    def get_lemma(self):
        return self.lemma

    def is_pos(self, pos):
        return self.pos == pos

    def get_frequency(self):
        return self.frequency

    def example(self):   # TODO: example = example.replace(self.lemma, 'XXXX')
        example = self.synset.examples()
        if example:
            example = example[0]
            example = example.replace(self.lemma, 'XXX') # TODO: Hide not only if lemma...
        return example

    def edit_distance(self, word_guess):
        return nltk.edit_distance(self.lemma, word_guess)

    def is_word(self, word_guess):
        return self.lemma == word_guess

    def definition(self):
        return self.synset.definition()

    def hypernym(self):
        return Word.__synset_to_string(self.synset.hypernyms())  # TODO: Names instead of just synset

    def hyponym(self):
        return Word.__synset_to_string(self.synset.hyponyms())

    def closest_hypernym(self, other_word):
        other_synset = wn.synsets(other_word)
        if other_synset:
            other_synset = other_synset[0]

            syn_lowest_hypernym = self.synset.lowest_common_hypernyms(other_synset)
            if syn_lowest_hypernym:
                return Word.__synset_to_string(syn_lowest_hypernym)[0]
        return Word.__synset_to_string(wn.synsets("word"))[0]

    def isEntity(self):
        other_synset = wn.synsets("entity")
        syn_lowest_hypernym = self.synset.lowest_common_hypernyms(other_synset)
        if syn_lowest_hypernym:
            return True
        return False

    def similarity_to(self, other_word):
        other_synset = wn.synsets(other_word)
        if other_synset:
            other_synset = wn.synsets(other_word)[0]
            return self.synset.wup_similarity(other_synset)
        else:
            return 0

    def print_all_synsets(self):
        for synset in wn.synsets(self.lemma):
            connections = Word.__syn_to_string(synset)
            for word in connections:
                if word != self.lemma:
                    print(word)
        return wn.synsets(self.lemma)

    def rhymes(self):
        rhyme = pronouncing.rhymes(self.lemma)
        if rhyme:
            return rhyme[0]
        return " "    # TODO: Prone to error

    @staticmethod
    def __synset_to_string(synset):
        return synset[0].lemma_names()

    @staticmethod
    def __syn_to_string(synset): # TODO: Ändra ful-lösning!!
        return synset.lemma_names()

