import csv
import sqlite3
import nltk
from nltk.stem import PorterStemmer # Import the PorterStemmer

# Connect to the database
conn = sqlite3.connect("index.db")
c = conn.cursor()

# Open a CSV file for writing
with open("data/documents.csv", "w", newline="") as f:
    # Create a writer object
    writer = csv.writer(f)
    # Write the header row
    writer.writerow(["name", "content"])
    # Write the data rows
    for row in c.execute("SELECT name, content FROM documents"):
        # Get the name and content of the document
        name = row[0]
        content = row[1]
        # Tokenize the content into a list of terms
        terms = nltk.word_tokenize(content)
        # Join the terms with commas
        terms = ",".join(terms)
        # Write the name and terms to the CSV file
        writer.writerow([name, terms])

# Close the connection
conn.close()
