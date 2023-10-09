import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))
stop_words |= set(stopwords.words('spanish'))

def get_word_frequencies(text):
    word_tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in word_tokens if word not in stop_words and word.isalnum()]
    frequencies = nltk.FreqDist(filtered_tokens)
    return dict(frequencies)
