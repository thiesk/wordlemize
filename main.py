import csv

RESET = '\033[0m'
BACKGROUND_BLACK = '\033[40m'
BACKGROUND_GREEN = '\033[42m'
BACKGROUND_YELLOW = '\033[43m'


class Wordlemizer:
    def __init__(self, word_base, tries=6):
        self.words = {}

        # list of (letter, reason, positions)
        self.known_letters = {}
        self.letter_scores = {}
        self.word_scores = {}
        self.not_known_letters = {}
        # -1 unknown, 0 in word, 1 correct
        self.history = []

        # load words from dataset into model
        with open(word_base, 'r') as words:
            reader = csv.reader(words)
            for word, freq in reader:
                if len(word) == 5:
                    self.words[word] = freq
                    for pos, letter in enumerate(word):
                        if letter not in self.letter_scores.keys():
                            self.letter_scores[letter] = [0, 0, 0, 0, 0]
                        self.letter_scores[letter][pos] += 1
        for word in self.words.keys():
            self.word_scores[word] = 0
            if len(set(word)) == len(word):
                for pos, letter in enumerate(word):
                    self.word_scores[word] += self.letter_scores[letter][pos]
        print(f"Loaded {len(self.words)} words")
        print(self.topk())

    def topk(self, k=5):
        top_k = []
        current_score = 0
        for word, score in self.word_scores.items():
            if current_score < score and len(set(word)) == len(word):
                best_word = word
                # top_k.append((best_word, score))
                top_k.append(best_word)
                if len(top_k) > k:
                    top_k.pop()
                current_score = score
        return list(reversed(top_k))

    def render(self):
        out = ""
        color = {-1: BACKGROUND_BLACK,
                 0: BACKGROUND_YELLOW,
                 1: BACKGROUND_GREEN}
        for word, feedback, n_words in self.history:
            for letter, action in zip(word, feedback):
                out += color[action] + letter + RESET
            out += f"  -->  Remaining words: {n_words}" + '\n'
        print(out)
        print(self.topk())


    def input(self, word, feedback):
        self.known_letters = {}
        for pos, letter in enumerate(word):
            self.__add_know_letter(letter, feedback[pos], [pos])
        self.__update()
        self.history.append((word, feedback, len(self.words)))

    def __add_know_letter(self, letter, reason, positions=None):
        self.known_letters[letter] = reason, positions

    def __update(self):
        self.__update_words()
        self.__update_letter_statistics()
        self.__update_letter_scores()
        self.__update_word_scores()

    def __update_word_scores(self):
        self.word_scores = {}
        for word in self.words.keys():
            self.word_scores[word] = 0
            for pos, letter in enumerate(word):
                self.word_scores[word] += len(self.not_known_letters[letter][pos])

    def __update_letter_scores(self):
        self.letter_scores = {}
        for word in self.words.keys():
            for pos, letter in enumerate(word):
                if letter not in self.letter_scores.keys():
                    self.letter_scores[letter] = set()
                self.letter_scores[letter] = self.letter_scores[letter].union(self.not_known_letters[letter][pos])

    def __update_letter_statistics(self):
        self.not_known_letters = {}
        for word in self.words.keys():
            for pos, letter in enumerate(word):
                if letter not in self.not_known_letters:
                    self.not_known_letters[letter] = [set()] * 5
                self.not_known_letters[letter][pos].add(word)

    def __update_words(self):
        remove = []
        for word in self.words.keys():
            gone = False
            # remove ruled out words
            for letter, (reason, positions) in self.known_letters.items():

                if gone:
                    break
                if letter in word:
                    # - letter should not be in word
                    if reason == -1 and letter in word:
                        remove.append(word)
                        break

                    # - partial letter in word
                    if reason == 0:
                        keep = False
                        # where letter should not be
                        for pos in positions:
                            # keep if it has remaining possible positions
                            if word[pos] == letter:
                                remove.append(word)
                                gone = True
                                break

                # - letter in correct positions
                if reason == 1:
                    for i in range(len(word)):
                        # remove words with any mismatch
                        if i in positions and not word[i] == letter or i not in positions and word[i] == letter:
                            remove.append(word)
                            gone = True
                            break

        for word in remove:
            del self.words[word]

class Player:
    def __init__(self):
        self.model = Wordlemizer("data/unigram_freq.csv")

    def play(self):
        while True:
            print('Type input to wordle.')
            word = input()
            print("Type output of wordle. Correct -> c; Wrong -> w; Wrong Position -> p")
            feedback = input()
            processed = []
            for info in feedback:
                if info == 'c':
                    processed.append(1)
                if info == 'w':
                    processed.append(-1)
                if info == 'p':
                    processed.append(0)

            self.model.input(word, processed)

            self.model.render()
            print("done")

if __name__ == '__main__':
    p = Player()
    p.play()