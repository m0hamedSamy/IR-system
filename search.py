

class Search:

    # Takes a string(phrase query) and the positional index of the document collection
    # Uses the get_documents_contain_the_word function
    # Returns the relevant documents to the query
    @staticmethod
    def get_relevant_docs(query, positional_index):
        query.lower()
        documents_of_each_word, relevant = [], []

        for word in query.split():
            documents_of_each_word.append(Search.__get_documents_contain_the_word(word, positional_index))

        intersected_documents = set(documents_of_each_word[0]).intersection(*documents_of_each_word)

        for document_name in intersected_documents:
            positions_of_words_in_this_document = []

            for word in query.split():
                positions_of_words_in_this_document.append(positional_index[word][document_name][:])

            for i in range(len(positions_of_words_in_this_document)):
                for j in range(len(positions_of_words_in_this_document[i])):
                    positions_of_words_in_this_document[i][
                        j] -= i  # makes all matched words positions have the same position number

            # if there is at least one match
            if len(set(positions_of_words_in_this_document[0]).intersection(*positions_of_words_in_this_document)) >= 1:
                relevant.append(document_name)

        return relevant

    # A simple query function that takes one word and
    # returns a list of all documents that have that word
    @staticmethod
    def __get_documents_contain_the_word(word, positional_index):
        word = word.lower()
        if word in positional_index.keys():
            return [document_name for document_name in positional_index[word].keys()]
        else:
            return []

