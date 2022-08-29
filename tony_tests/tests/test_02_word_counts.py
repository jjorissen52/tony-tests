import random
from english_words import english_words_alpha_set

from tony_tests.tests.utils import import_solution

word_counts = import_solution("word_counts")
whitespace = [' ', '\n', '\t']


def test_word_counts():
    words = random.choices(list(english_words_alpha_set), k=random.randint(1000, 10000))
    string = words[0]
    for word in words:
        string += "".join(random.choices(whitespace, k=random.randint(1, 10))) + word

    solution_counts = word_counts(string)

    words = [w.lower() for w in string.split() if w]
    counts = {word: words.count(word) for word in set(words)}

    assert solution_counts == counts
