import pandas as pd
import math
from collections import Counter
import pandas as pd
import math

def vector_process_documents(documents_file="data/documents.csv"):
    """Reads and processes documents from the specified CSV file."""
    documents = pd.read_csv(documents_file)
    rows = len(documents)
    cols = len(documents.columns)
    idf = {}
    vectors = {}

    # Store terms, document names, and vectors in a single dictionary
    for i in range(rows):
        doc_name = documents.loc[i].iat[0]
        terms = list(documents.loc[i][1:])
        terms = sorted(terms)  # Remove duplicates and sort
        vectors[doc_name] = {"terms": terms, "vector": None}

    # Compute term frequencies (tf) and inverse document frequencies (idf)
    term_freq = {}  # Initialize term_freq here
    for doc_name, doc_data in vectors.items():  # Iterate through all documents
        for term in doc_data["terms"]:
                term_freq[term] = term_freq.get(term, 0) + 1  # Count all occurrences
    print("term_freq: \n", term_freq, "\n")
    for term in term_freq:
        idf[term] = math.log(cols / term_freq[term])

    # Compute tf-idf weights for each term in each document
    for doc_name, doc_data in vectors.items():
        weight_vector = []
        for term in doc_data["terms"]:
            weight = term_freq[term] / cols * idf[term]
            weight_vector.append(weight)
        vectors[doc_name]["vector"] = weight_vector
    print("vectors : \n", vectors, "\n \n")
    return vectors, idf  # Return both vectors and idf


def vector_search(query, vectors,idf):
    """Performs vector-based search and returns ranked results."""
    query_terms = query.split(" ")
    query_vector = [idf.get(term, 0) for term in query_terms]  # Use idf for query terms
    print("vectors in vector_search: \n", vectors)
    results = prediction(query_vector, vectors)
    return results

def prediction(query_vector, vectors):
    """Predicts relevant documents based on query vector."""
    dictionary = {}
    for doc_name, doc_data in vectors.items():
        doc_vector = doc_data["vector"]

        numerator = sum(q_val * d_val for q_val, d_val in zip(query_vector, doc_vector))
        denominator = (sum(q_val**2 for q_val in query_vector) *
                       sum(d_val**2 for d_val in doc_vector))**0.5

        if denominator != 0:
            simi = numerator / denominator
            dictionary[doc_name] = simi

    sorted_results = [(doc_name, rank + 1) for rank, (doc_name, score) in enumerate(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))]
    return sorted_results
