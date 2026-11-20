
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer


# Initialize NLP tools
tokenizer = TreebankWordTokenizer()
lemmatizer = WordNetLemmatizer()

# Load English stop words
stop_words = set(stopwords.words("english"))

# Preserve negation words because they can change meaning
important_words = {"no", "not", "nor", "never"}

stop_words = stop_words - important_words


def preprocess_text(text):

    # 1. Convert text into lowercase
    text = text.lower()

    # 2. Remove punctuation and special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # 3. Tokenization
    tokens = tokenizer.tokenize(text)

    # 4. Remove stop words and perform lemmatization
    processed_tokens = []

    for word in tokens:

        if word not in stop_words:

            lemma = lemmatizer.lemmatize(word)

            processed_tokens.append(lemma)

    # Convert tokens back into a sentence
    cleaned_text = " ".join(processed_tokens)

    return cleaned_text
