from math import log
from math import sqrt


class Rank:

    @staticmethod
    def rank_results(query, document_collection, positional_index, relevant_docs):
        normalize_matrix = Rank.__get_normalize_matrix(query, document_collection, positional_index)
        similarity = {}
        for i in range(len(normalize_matrix) - 1):
            doc_normalize = 0
            for j in range(len(normalize_matrix[document_collection[i]])):
                doc_normalize += float(normalize_matrix[document_collection[i]][j]) * float(normalize_matrix["query"][j])
            similarity[document_collection[i]] = doc_normalize

        similarity_of_relevant_docs = {}
        for document in relevant_docs:
            similarity_of_relevant_docs[document] = similarity.get(document)

        similarity_of_relevant_docs = sorted(similarity_of_relevant_docs.items(), key=lambda x: x[1], reverse=True)

        return similarity_of_relevant_docs

    @staticmethod
    def __get_normalize_matrix(query, document_collection, positional_index):
        normalize_matrix = {}
        for document in document_collection:
            normalize_list_of_terms = []
            for term in positional_index.keys():
                normalize_list_of_terms.append(
                    Rank.__normalize_doc(term, document, positional_index, len(document_collection)))
            normalize_matrix[document] = normalize_list_of_terms

        normalize_list_of_query = []
        for term in positional_index.keys():
            normalize_list_of_query.append(Rank.__normalize_query(term, query, positional_index, len(document_collection)))

        normalize_matrix["query"] = normalize_list_of_query
        return normalize_matrix

    @staticmethod
    def __normalize_doc(term, document, positional_index, number_of_docs):
        tf_idf = Rank.__get_tf_idf(term, document, positional_index, number_of_docs)
        doc_length = Rank.__get_document_length(document, positional_index, number_of_docs)
        return tf_idf / doc_length

    @staticmethod
    def __normalize_query(term, query, positional_index, number_of_docs):
        tf_idf = Rank.__get_tf_idf_query(term, query, positional_index, number_of_docs)
        query_length = Rank.__get_query_length(query, positional_index, number_of_docs)
        return tf_idf / query_length

    @staticmethod
    def __get_document_length(document, positional_index, number_of_docs):
        squared_idf_sum = 0
        for term in positional_index.keys():
            tf_idf = Rank.__get_tf_idf(term, document, positional_index, number_of_docs)
            squared_idf_sum += (tf_idf * tf_idf)

        return sqrt(squared_idf_sum)

    @staticmethod
    def __get_query_length(query, positional_index, number_of_docs):
        squared_idf_sum = 0
        for term in positional_index.keys():
            tf_idf = Rank.__get_tf_idf_query(term, query, positional_index, number_of_docs)
            squared_idf_sum += (tf_idf * tf_idf)

        return sqrt(squared_idf_sum)

    @staticmethod
    def __get_tf_idf(term, document, positional_index, number_of_docs):
        tf_w = Rank.__get_tf_weight(term, document, positional_index)
        idf = Rank.__get_idf_of_term(term, positional_index, number_of_docs)
        return tf_w * idf

    @staticmethod
    def __get_tf_idf_query(term, query, positional_index, number_of_docs):
        tf_w = Rank.__get_tf_weight_query(term, query)
        idf = Rank.__get_idf_of_term(term, positional_index, number_of_docs)
        return tf_w * idf

    @staticmethod
    def __get_idf_of_term(term, positional_index, number_of_docs):
        df = Rank.__get_document_frequency_of_term(term, positional_index)
        return log(number_of_docs / df, 10)

    @staticmethod
    def __get_tf_weight(term, document, positional_index):
        tf = Rank.__get_term_frequency_in_doc(term, document, positional_index)
        if tf > 0:
            return 1 + log(tf, 10)
        else:
            return 0

    @staticmethod
    def __get_tf_weight_query(term, query):
        tf = Rank.__get_term_frequency_in_query(term, query)
        if tf > 0:
            return 1 + log(tf, 10)
        else:
            return 0

    @staticmethod
    def __get_document_frequency_of_term(term, positional_index):
        doc_count = 0
        for doc_dict in positional_index[term]:
            doc_count += 1

        return doc_count

    @staticmethod
    def __get_term_frequency_in_doc(term, document, positional_index):
        tf = 0
        if document in positional_index[term]:
            tf = len(positional_index[term][document])

        return tf

    @staticmethod
    def __get_term_frequency_in_query(term, query):
        query = query.lower().split()
        count = 0
        for word in query:
            if word == term:
                count += 1

        return count
