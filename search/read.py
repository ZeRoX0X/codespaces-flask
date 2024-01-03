import csv
import sqlite3
import nltk
from nltk.stem import PorterStemmer # Import the PorterStemmer
import os


def read_documents_to_csv():
    """Reads documents from the database and writes them to a CSV file."""

    try:
        # Connect to the database
        conn = sqlite3.connect("index.db")
        c = conn.cursor()

        # Open the CSV file for writing
        with open("data/documents.csv", "w", newline="") as f:
            writer = csv.writer(f)

            # Write the header row
            writer.writerow(["name", "content"])

            # Write the data rows
            for row in c.execute("SELECT name, content FROM documents"):
                name = row[0]
                content = row[1]

                # Tokenize the content
                terms = nltk.word_tokenize(content)

                # Join the terms with commas
                terms_str = ",".join(terms)

                # Write the name and terms to the CSV file
                writer.writerow([name, terms_str])

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    except FileNotFoundError:
        print(f"Error creating CSV file: {e}")

    finally:
        conn.close()  # Ensure database connection is closed

def retrieve_document_text(document_name):
    """Retrieves the original text of a document from the database or file."""

    try:

        text_dir = "data/extracted_texts"
        text_file = os.path.join(text_dir, document_name + ".txt")
        if os.path.exists(text_file):
            with open(text_file, "r", encoding="utf-8") as f:
                document_text = f.read()
            return document_text

        # If not found in either database or file, raise an exception
        raise ValueError(f"Document '{document_name}' not found")

 

    except FileNotFoundError:
        print(f"Extracted text file not found for document '{document_name}'")
        return None