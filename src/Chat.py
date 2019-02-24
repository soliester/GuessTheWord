from string import punctuation
from nltk.corpus import wordnet as wn


def preprocess_text(sentence):
    sentence = sentence.lower()
    for p in punctuation:
        sentence = sentence.replace(p, '')
    return sentence


def indicators():
    return {
        **dict.fromkeys(['noun', 'nn', 'thing', 'object', 'nn', 'verb', 'action', 'occurence',
                         'adjective', 'describe', 'describes', 'description', 'numeral', 'preposition',
                         'adverb', 'pronoun', 'conjunction', 'determiner', 'exclamation'], 'spec_pos'),

        **dict.fromkeys(['class', 'part of speech', 'pos', 'category', 'type', 'kind of'], 'pos_type'),

        **dict.fromkeys(['clue', 'random', 'hint'], 'clue'),

        **dict.fromkeys(['context', 'situation', 'situations', 'example', 'use', 'used', 'usage', 'next to'],
                        'context'),

        **dict.fromkeys(['similar', 'relate', 'relationship', 'correlate', 'remind', 'synonym'], 'similar'),

        **dict.fromkeys(['common', 'often', 'occur', 'often', 'frequency'], 'frequency'),

        **dict.fromkeys(['length', 'amount', 'long', 'consist', 'many', 'characters', 'letters'], 'length'),

        **dict.fromkeys(['first', 'start', 'starts', '1st'], 'first'),

        **dict.fromkeys(['second', '2nd'], 'second'),

        **dict.fromkeys(['last', 'end', 'ends', 'ending', 'final', 'finish', 'conclude'], 'last'),

        **dict.fromkeys(['third', 'fourth', 'fifth', 'sixth', '3rd', '4th', '5th'], 'illegal'),

        **dict.fromkeys(['i think', 'guess'], 'guess'),

        **dict.fromkeys(['stop', 'quit', 'give up', 'done', 'exit'], 'stop'),
    }


def pos_indicators():
    return {
        **dict.fromkeys(['noun', 'thing', 'object'], 'noun'),

        **dict.fromkeys(['verb', 'you do' 'action', 'occurence'], 'verb'),

        **dict.fromkeys(['adjective', 'describe', 'describes', 'description'], 'adjective'),

        **dict.fromkeys(['preposition'], 'preposition'),

        **dict.fromkeys(['numeral'], 'numeral'),

        **dict.fromkeys(['adverb'], 'adverb'),

        **dict.fromkeys(['conjunction'], 'conjunction'),

        **dict.fromkeys(['determiner'], 'determiner'),

        **dict.fromkeys(['exclamation'], 'exclamation'),
    }


def match_input(sentence, game_word):
    sentence = preprocess_text(sentence)
    for word in sentence.split():
        if word in indicators():
            return respond(indicators().get(word), word, game_word, sentence)


def respond(indicating_word, base_word, game_word, sentence):  # TODO: Refactor variable names
    if indicating_word is indicators().get('noun'):
        pos = pos_indicators().get(base_word)
        article = get_indefinite_article(base_word)  # TODO: Check if works...

        if game_word.is_pos(pos):
            return "Yes, it's " + article + " " + pos  # TODO: a or an!
        else:
            return "No, it's not " + article + " " + pos

    elif indicating_word is indicators().get('class'):
        pos = game_word.get_pos()
        if pos:
            return "It's a " + pos
        else:
            return "Damn"

    elif indicating_word is indicators().get('context'):
        context = game_word.example()
        if context:
            return context
        else:
            return "Oh, I can't come up with any examples :("

    elif indicating_word is indicators().get('similar'):
        sentence = sentence.split()
        comparison_word = sentence[-1]  # Heuristic solution, other solution possible?

        if not comparison_word == "to":
            similarity = game_word.similarity_to(comparison_word)
            if similarity is not None:
                if similarity == 1:
                    return "They're not similar, they are the same :)"
                elif 0.5 < similarity < 1:
                    closest_hypernym = game_word.closest_hypernym(comparison_word)
                    return "Yeah, they are both a type of " + closest_hypernym
                elif 0.2 <= similarity <= 0.5:
                    closest_hypernym = game_word.closest_hypernym(comparison_word)
                    return "There's some similarities, they are both a type of " + closest_hypernym
                else:
                    return "I can't see any similarities with " + comparison_word

        else:
            return "Dunno"

    elif indicating_word is indicators().get('first'):
        return "The first letter is " + game_word.first_letter()

    elif indicating_word is indicators().get('second'):
        return "The second letter is " + game_word.second_letter()

    elif indicating_word is indicators().get('last'):
        return "The last letter is " + game_word.last_letter()

    elif indicating_word is indicators().get('third'):
        return "Huh, stop asking questions like that!"

    elif indicating_word is indicators().get('long'):
        return "The word has " + str(game_word.length()) + " letters"

    elif indicating_word is indicators().get('common'):
        frequency = game_word.get_frequency()

        if frequency < 150:
            return "It's very common"
        elif 150 < frequency < 300:
            return "It's fairly common"
        else:
            return "It's not that common"

    elif indicating_word is indicators().get('clue'):
        return "Might rhyme with " + game_word.rhymes()

    elif indicating_word is indicators().get('stop'):
        exit()

    elif indicating_word is indicators().get('guess'):
        sentence = sentence.split()
        comparison_word = wn.synsets(sentence[-1])
        if comparison_word:
            comparison_word = comparison_word[0].lemma_names()[0]
            if comparison_word == game_word.get_lemma():
                return "correct"
        return "Nope!"


# Simple solution that works in this case
def get_indefinite_article(word):
    vowels = ["a", "e", "i", "o", "u"]
    return "an" if word[0] in vowels else "a"
