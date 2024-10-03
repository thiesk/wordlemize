import csv
import numpy as np

class wordlemizer():
    def __init__(self, word_base, tries = 6):
        self.words = {}
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
                        self.letters[letter]
                    self.words[word] = freq


    def update_words(self, results):
        for word in self.words.keys():
            # remove ruled out words
            for letter, reason, positions in results:
                # - letter not in word
                if reason == -1 and letter in word:
                    del self.words[word]

                # - letter in word but position is wrong
                if reason == 0:
                    keep = False
                    for pos in positions:
                        if not word[pos] == letter:
                            keep = True
                    if not keep:
                        del self.words[word]

                if reason == 1 and not letter in word:
                    del self.words[word]
            # recalculate letter statistics

    def get_letter_statistics(self):
        for word in self.words.keys():
            for position, letter in enumerate(word):
                if not letter in self.letters.keys():
                    self.letters[letter] = {"count": 0, "count in pos": []}
                self.letters[letter]["count"] += 1

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
