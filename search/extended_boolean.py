import pandas as pd
import math

# Global variables


def extended_process_documents():
    """Reads and processes documents from the CSV file."""
    terms = []
    keys = []
    vec_dic = {}
    term_freq = {}
    doc_freq = {}
  
    documents = pd.read_csv("data/documents.csv")
    rows = len(documents)
    cols = len(documents.columns)
    num_documents = rows

    dicti = {}
    for i in range(rows):
        keys.append(documents.loc[i].iat[0])
        dicti[documents.loc[i].iat[0]] = list(documents.loc[i][1:])

        for term in documents.loc[i][1:]:
            if term not in terms:
                terms.append(term)
            term_freq[term] = term_freq.get(term, 0) + 1
            doc_freq[term] = doc_freq.get(term, 0) + 1

    terms.sort()
    for doc_name, terms_list in dicti.items():
        bool_vec = [term_weight(term,term_freq,num_documents,doc_freq) for term in terms]  # Use TF-IDF weights
        vec_dic[doc_name] = bool_vec
    print(terms, "\n \n \n")
    print("term_freq: \n",term_freq)
    return term_freq,num_documents,doc_freq,vec_dic,terms

def term_weight(term,term_freq,num_documents,doc_freq):
    """Returns the TF-IDF weight of a term."""
    tf = term_freq[term] / num_documents
    idf = math.log(num_documents / doc_freq[term])
    return tf * idf

def extended_boolean_search(query,term_freq,num_documents,doc_freq,vec_dic,terms):
    """Performs extended boolean search with term weights."""
    query_terms = query.split(" ")
    q_vect = [term_weight(term,term_freq,num_documents,doc_freq) for term in query_terms]

    results = {}
    for doc_name, doc_vec in vec_dic.items():
        score = 0
        for i in range(len(terms)):
            if q_vect[i] > 0 and doc_vec[i] > 0:
                score += q_vect[i] * doc_vec[i]
        results[doc_name] = score

    sorted_results = [(doc_name, rank + 1) for rank, (doc_name, score) in enumerate(sorted(results.items(), key=lambda item: item[1], reverse=True))]
    return sorted_results

