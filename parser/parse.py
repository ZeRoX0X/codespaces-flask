import sqlite3
from docx import Document
def parse(file):
    # Open the doc file and extract the text
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])

    # Connect to the sqlite database and create a table
    conn = sqlite3.connect("index.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, name TEXT, content TEXT)")

    # Insert the text into the table
    c.execute("INSERT INTO documents (name, content) VALUES (?, ?)", ("example.docx", text))
    conn.commit()

    # Close the connection
    conn.close()
    isParsed = True
    return isParsed
