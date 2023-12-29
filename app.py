from flask import Flask, render_template, request, jsonify
from docx import Document
import os
from docparse import parsedoc
import tempfile

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="DuckDuckGo")

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the uploaded files dictionary
    files = request.files.getlist("doc_files")
    # Iterate over the files
    for file in files:
        # Save each file to the folder
        file.save("data/" + file.filename)
        # Get the file path
        file_path = "data/" + file.filename
        # Parse the file content
        isParsed = parsedoc(file_path)
        # Check the parsing result
        if isParsed == True:
            print("parse success")
        else:
            print("parse failed")
    # Return a response
    return render_template("search.html", title="Search")

@app.route('/search')
def search():
    return