import csv

RESET = '\033[0m'
BACKGROUND_BLACK = '\033[40m'
BACKGROUND_RED = '\033[41m'
BACKGROUND_GREEN = '\033[42m'
BACKGROUND_YELLOW = '\033[43m' # orange on some systems
BACKGROUND_BLUE = '\033[44m'
BACKGROUND_MAGENTA = '\033[45m'
BACKGROUND_CYAN = '\033[46m'
BACKGROUND_LIGHT_GRAY = '\third-party033[47m'
BACKGROUND_DARK_GRAY = '\033[100m'
BACKGROUND_BRIGHT_RED = '\033[101m'
BACKGROUND_BRIGHT_GREEN = '\033[102m'
BACKGROUND_BRIGHT_YELLOW = '\033[103m'
BACKGROUND_BRIGHT_BLUE = '\033[104m'
BACKGROUND_BRIGHT_MAGENTA = '\033[105m'
BACKGROUND_BRIGHT_CYAN = '\033[106m'
BACKGROUND_WHITE = '\033[107m'

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
        self.__update_letter_statistics()
        print(f"Loaded {len(self.words)} words")

    def topk(self, k=10):
        top_k = []
        current_score = 0
        for word, score in self.word_scores.items():
            if current_score < score:
                best_word = word
                top_k.append((best_word, score))
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
        print(model.topk())


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
                    if reason == -1:
                        for i in range(len(word)):
                            # remove words with any mismatch
                            if i in positions and word[i] == letter:
                                remove.append(word)
                                gone = True
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
                        continue

                # - letter in correct positions
                if reason == 1:
                    for i in range(len(word)):
                        # remove words with any mismatch
                        if i in positions and not word[i] == letter or i not in positions and word[i] == letter:
                            remove.append(word)
                            gone = True
                            break
                    continue

        for word in remove:
            del self.words[word]


if __name__ == '__main__':
    model = Wordlemizer("data/unigram_freq.csv")

    model.input("pilot", [-1, -1, -1, 1, -1])
    model.input("major", [-1, 1, -1, 1, -1])
    model.input("canon", [-1, 1, -1, 1, 1])

    model.render()
