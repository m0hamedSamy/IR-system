import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class Preprocessing:

    # Takes a file name and its language.
    # Returns a list of all tokens (cleaned from all stopwords and punctuations) in that file
    @staticmethod
    def __tokenize(document, language):
        stop_words = set(stopwords.words(language.lower()))
        punctuations = set(string.punctuation)

        file = open("DocumentCollection\\" + document.lower(), "r")

        tokens = word_tokenize(file.read(), language)
        tokens = " ".join(tokens).lower().split()  # converting all tokens to lower case
        # cleaning tokens (removing stopwords and punctuations from tokens)
        tokens = [token for token in tokens if token not in (stop_words and punctuations) and ("'" not in token)]
        return tokens

    # Takes a list of document names
    # Uses tokenize function to extract a list of tokens from each document
    # Returns a map where each document name mapped to its token list
    @staticmethod
    def documents_to_terms(document_names):
        index = {}
        for document in document_names:
            tokens = Preprocessing.__tokenize(document, "English")
            index[document] = tokens
        return index

