from utils.frequencies import get_word_frequencies
class Scorer:
    @staticmethod
    def score(text, title, h1, description):
        frequencies = get_word_frequencies(text)
        scores = {}
        for word, frequency in frequencies.items():
            score = frequency
            if word in title.lower(): score += 100
            if h1 and word in h1.lower(): score += 100
            if word in description.lower(): score += 100
            scores[word] = score
        return scores