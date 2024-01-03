from flask import Flask, render_template, request, jsonify
from docx import Document
import os
from docparse import parsedoc, preprocess_arabic,preprocess_english
import tempfile
from search.boolean import boolean_search, boolean_process_documents
from search.extended_boolean import extended_boolean_search, extended_process_documents
from search.vector_space import vector_search,vector_process_documents
from search.read import retrieve_document_text

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST']) 
def home():
    if request.method == 'POST':
        try:
            upload_file()  # Call the upload_file function
            return render_template("index.html", title="DuckDuckGo")
           
        except Exception as e:
            return f"Error: {e}"  # Return error message if any
    else:
        return render_template("index.html", title="DuckDuckGo")
    
def upload_file():
    files = request.files.getlist("doc_files")
    for file in files:
        filename = file.filename
        file.save(os.path.join("data", filename)) 

        file_path = os.path.join("data", filename)
        if parsedoc(file_path, "en"):
            print("Parse success:", filename)
        else:
            print("Parse failed:", filename)


@app.route("/search")
def search():
    query = request.args.get("q")
    model = request.args.get("model")
    procced_query,_ = preprocess_english(query)
    print(procced_query)
    if model == "Boolean":
        terms,vec_dic = boolean_process_documents()
        results = boolean_search(procced_query,terms,vec_dic)
        print(results)
    elif model == "Extended Boolean":
        term_freq,num_documents,doc_freq,vec_dic,terms = extended_process_documents()
        results = extended_boolean_search(procced_query,term_freq,num_documents,doc_freq,vec_dic,terms)
        print(results)
    elif model == "Vector":
        vectors,idf =  vector_process_documents()
        results = vector_search(procced_query,vectors,idf)
        print(results)
       
        
    else:
        return jsonify({"error": "Invalid model"}), 400

    return jsonify(results)

@app.route("/document/<document_name>")
def get_document_text(document_name):
    # Retrieve document text from your data source or file
    document_text = retrieve_document_text(document_name)
    return document_text