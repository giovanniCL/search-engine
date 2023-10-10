from utils.frequencies import get_word_frequencies
class Scorer:
    @staticmethod
    def score(text, title):
        frequencies = get_word_frequencies(text)
        scores = {}
        for word, frequency in frequencies.items():
            score = frequency
            if word in title.lower(): score += 100
            scores[word] = score
        return scores