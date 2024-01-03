import pandas as pd

# Global variables (consider moving to a configuration module if needed)


def boolean_process_documents():
    """Reads and processes documents from the CSV file."""
    documents = pd.read_csv("data/documents.csv")
    rows = len(documents)
    cols = len(documents.columns)
    terms = []
    dicti = {}
    keys = []
    vec_dic = {}

    for i in range(rows):
        keys.append(documents.loc[i].iat[0])
        dicti[documents.loc[i].iat[0]] = list(documents.loc[i][1:])

        for term in documents.loc[i][1:]:
            if term not in terms:
                terms.append(term)

    terms.sort()
    for doc_name, terms_list in dicti.items():
        bool_vec = [1 if term in terms_list else 0 for term in terms]
        vec_dic[doc_name] = bool_vec
    return terms,vec_dic

def boolean_search(query,terms,vec_dic):  # Renamed function
    """Performs boolean search and returns matching documents."""
    query_terms = query.split(" ")
    q_vect = [1 if term in query_terms else 0 for term in terms]
    results = prediction(q_vect,vec_dic)
    return results

def prediction(q_vect,vec_dic):
    """Predicts relevant documents based on query vector."""
    dictionary = {}
    for doc_name, doc_vec in vec_dic.items():
        count = sum(q_val == doc_val for q_val, doc_val in zip(q_vect, doc_vec))
        dictionary[doc_name] = count

    sorted_results = [(doc_name, rank + 1) for rank, (doc_name,count)  in enumerate(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))]

    return sorted_results
