from flask import Flask, render_template, request
from docx import Document

from parser import parse
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="DuckDuckGo")

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the uploaded file object
    file = request.files['doc_file']
    # Save the file to a local directory
    file.save('example.docx')
    # Or read the file content using python-docx
    isParsed = parse(file)
    return isParsed
