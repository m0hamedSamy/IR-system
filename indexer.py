from preprocessing import Preprocessing


class Indexer:

    # Takes a list of terms in a document
    # Returns a map where each term mapped to its positions in a document
    @staticmethod
    def __index_one_document(document_terms):
        document_index = {}
        for index, term in enumerate(document_terms):
            if term in document_index.keys():
                document_index[term].append(index)
            else:
                document_index[term] = [index]
        return document_index

    # Uses the map created by documents_to_terms function and the map
    # created by index_one_file function.
    # Returns a map where each document mapped to a map of the terms in that document
    # where each term mapped to its positions in that document.
    @staticmethod
    def __index_all_documents(document_names):
        index = {}
        document_terms_map = Preprocessing.documents_to_terms(document_names)
        for document in document_terms_map.keys():
            index[document] = Indexer.__index_one_document(document_terms_map[document])
        return index

    # Uses the map created by index_all_documents function.
    # returns a positional index where each term mapped to a map of documents (that have
    # that term) where each document mapped to list of positions of that term in this document.
    @staticmethod
    def pos_index(document_names):
        document_terms_pos = Indexer.__index_all_documents(document_names)
        index = {}
        for document in document_terms_pos.keys():
            for term in document_terms_pos[document].keys():
                if term in index.keys():
                    index[term][document] = document_terms_pos[document][term]
                else:
                    index[term] = {document: document_terms_pos[document][term]}
        return index

