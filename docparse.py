import sqlite3
import textract
import os
import csv
import antiword
import nltk  # Import NLTK for preprocessing
from nltk.stem import PorterStemmer  # Import Porter stemmer
from nltk.corpus import stopwords  # Import stopword list

nltk.download("punkt")  # Download necessary NLTK resources
nltk.download("stopwords")

stemmer = PorterStemmer()  # Create a stemmer instance
stop_words = set(stopwords.words("english"))  # Load English stopwords

def parsedoc(file):
    try:
        # Extract the text from the file using textract
        text = textract.process(file).decode("utf-8")

        # Preprocess the text
        preprocessed_text = preprocess_english(text)

        # Connect to the SQLite database
        conn = sqlite3.connect("index.db")
        c = conn.cursor()

        # Create the documents table with FTS5 indexing
        c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(name, content)")

        # Insert the preprocessed text into the FTS5 table
        c.execute("INSERT INTO documents (name, content) VALUES (?, ?)", (file, preprocessed_text))
        conn.commit()

        conn.close()
        return True

    except (textract.exceptions.ExtensionNotSupported, textract.exceptions.MissingFileError) as e:
        print(f"Error processing file: {e}")
        return False

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

    finally:
        print("Parsing finished")

def preprocess_english(text):
    """Preprocesses English text for search."""
   
    # Remove punctuation
    tokens = [token.translate(str.maketrans('', '', string.punctuation)) for token in tokens]
    tokens = nltk.word_tokenize(text.lower())  # Tokenize and lowercase
    filtered_tokens = [token for token in tokens if token not in stop_words]  # Remove stop words
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]  # Stem words
    preprocessed_text = " ".join(stemmed_tokens)  # Rejoin tokens
    return preprocessed_text
