from src.WordFinder import WordFinder
from src.Word import Word
from src import Chat

wf = WordFinder.get_word()
word = Word(wf[0], wf[1], wf[2])

print("Hey! I have a word just for you! :)\n"
      "C'mon and ask a question about it!\n"
      "Examples of questions I can understand:\n"
      "\tHow many letters does the word have?\n"
      "\tIs it similar to apple?\n"
      "\tIs it a noun?\n\n"
      
      "Some questions I don't understand:\n"
      "\tIs it a type of animal?\n"
      "\tIs it in the room?\n"
      "Sorry 'bout that :(\n\n"
      
      "Guess by writing the word 'guess' and a word, like this:\n"
      "\tguess apple\n")


def is_correct(guess):
    for w in guess.split():
        if w == word:
            print(w, " ", word)
            return True
        else:
            return False


def game():
    word_guessed = False
    game_round = 1
    max_round = 10

    while game_round <= max_round and not word_guessed:
        guess = input("Guess " + str(game_round) + "/" + str(max_round) + ": ")
        answer = Chat.match_input(guess, word)

        if answer is not None:
            if answer is not "correct":
                print(answer)
            else:
                word_guessed = True
            game_round += 1

    if word_guessed:
        print("YOU WON!!! :)")
    else:
        print("Times up, the word was " + word.get_lemma())


game()
