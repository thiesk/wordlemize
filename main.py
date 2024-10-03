import csv
import numpy as np

class wordlemizer():
    def __init__(self, word_base, tries = 6):
        self.words = {}
        self.max_tries = tries
        self.tries = 0
        self.letters = {}
        self.guessed_letters = []

        # -1 unknown, 0 in word, 1 correct
        self.state = -np.ones((tries, 5))
        self.letter_state = [-1, -1, -1, -1, -1]
        with open(word_base, 'r') as words:
            reader = csv.reader(words)
            first_guess = False
            for i, (word, freq) in enumerate(reader):
                if len(word) == 5:
                    if not first_guess:
                        first_guess = word
                    for position, letter in enumerate(word):
                        if not letter in self.letters.keys():
                            self.letters[letter] = {"count": 0, "count in pos": []}
                        self.letters[letter]["count"] += 1
                        self.letters[letter]
                    self.words[word] = freq

        self.guess = first_guess
        print(f"My first guess: {first_guess}")

    def enter_guess(self, results):
        wrong, partial, right = results
        for word in self.words.keys():
            # select only possibly correct words
            # - fully correct letters
            for letter, pos in right:
                if word[pos] == letter:
                    break
            if not relevant:
                del self.words[word]
                continue

            # - correct letter; wrong position
            for letter, pos in partial:
                if not word[pos] == letter:


            # - delete impossible words
            for letter, pos in wrong:
                if word[pos] == letter:
                    del self.words[word]
        # recalculate letter statistics
        for letter, pos in wrong:
            del self.letters[letter]

    def get letter statistics
    def word_score(self, word):
        score = 0
        for letter in word:
            remaining_letters = list(self.letters.keys())
            n_positions = np.sum(self.state[self.state == 1], axis=1)[self.tries]
            for known in self.guessed_letters:
                remaining_letters.remove(known)
            if letter in remaining_letters:
                score += self.letters[letter]
        return score / n_positions

    def set_guess(self, position, letter):
        if self.state[position, self] < 1:
            self.guess[position] = letter
        else:
            print(f"position {position} is already correct")



if __name__ == '__main__':
    wordlemizer("data/unigram_freq.csv")
