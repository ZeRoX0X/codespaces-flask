import sqlite3
import textract
import os
import csv
import antiword
import nltk  # Import NLTK for preprocessing
from nltk.stem import PorterStemmer  # Import Porter stemmer
from nltk.corpus import stopwords  # Import stopword list
from nltk.stem.isri import ISRIStemmer  # Import ISRIStemmer for Arabic stemming
import string
nltk.download("punkt")  # Download necessary NLTK resources
nltk.download("stopwords")

stemmer = PorterStemmer()  # Create a stemmer instance
stop_words = set(stopwords.words("english"))  # Load English stopwords

def parsedoc(file, lan="en"): 
    try:
        # Extract the text from the file using textract
        text = textract.process(file).decode("utf-8")
        
        text_dir = "data/extracted_texts"  # Replace with desired directory name
        if not os.path.exists(text_dir):
                os.makedirs(text_dir)
        # Save original text to a file
        text_file = os.path.join(text_dir, os.path.basename(file) + ".txt")  # Create filename preserving original extension
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text)
        
        
        if lan == "en":
            # Preprocess the text
            preprocessed_text,stemmed_tokens = preprocess_english(text)
        else:
            preprocessed_text,stemmed_tokens  = preprocess_arabic(text)
        # Connect to the SQLite database
        conn = sqlite3.connect("index.db")
        c = conn.cursor()

        # Create the documents table with FTS5 indexing
        c.execute("CREATE  TABLE IF NOT EXISTS documents(name, content)")
        
        c.execute("CREATE  TABLE IF NOT EXISTS documents_index(term TEXT, name TEXT, positions TEXT)")
        
        

        
        
        c.execute("INSERT INTO documents (name, content) VALUES (?, ?)", (file, preprocessed_text))
        
        with open("data/documents.csv", "a", newline="") as f:  # Open in append mode
            writer = csv.writer(f)
            # Join the terms with commas
            terms = ",".join(stemmed_tokens)
            writer.writerow([os.path.basename(file), terms])

        # Insert into index table
        terms = preprocessed_text.split()  # Simple tokenization for this example
        positions = []
        for i, term in enumerate(terms):
            positions.append((i, i + len(term)))  # Store start and end positions
        c.executemany("INSERT INTO documents_index VALUES (?, ?, ?)", [(term, file, str(pos)) for term, pos in zip(terms, positions)])

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
    tokens = nltk.word_tokenize(text.lower())  # Tokenize and lowercase
    tokens = [token.translate(str.maketrans('', '', string.punctuation)) for token in tokens]  # Remove punctuation
    filtered_tokens = [token for token in tokens if token not in stop_words]  # Remove stop words
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]  # Stem words
    preprocessed_text = " ".join(stemmed_tokens)  # Rejoin tokens
    return preprocessed_text, stemmed_tokens


def preprocess_arabic(text):
    """Preprocesses Arabic text for search using NLTK."""



    # Tokenize
    tokens = nltk.word_tokenize(text)

    # Remove punctuation
    punctuation = list("»«،؛؟.")  
    tokens = [token for token in tokens if token not in punctuation]

    # Remove stop words (optional)
    stop_words = set(nltk.corpus.stopwords.words("arabic"))  # Load Arabic stopwords
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Stemming (optional)
    stemmer = ISRIStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]

    # Rejoin tokens
    preprocessed_text = " ".join(stemmed_tokens)

    return preprocessed_text, stemmed_tokens