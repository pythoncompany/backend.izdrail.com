from fastapi import APIRouter, Path, Query, Depends
from pydantic import BaseModel
from cachetools import TTLCache
import os
from seoanalyzer import analyze
from lighthouse import LighthouseRunner
from fastapi import FastAPI, File, UploadFile
import pymupdf4llm
import spacy
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk
import random
nltk.download('averaged_perceptron_tagger')

# Directory to save the uploaded PDFs
UPLOAD_DIRECTORY = "pdfs"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
router = APIRouter()
lemmatizer = WordNetLemmatizer()

class RewriteText(BaseModel):
    text: str

nlp = spacy.load("en_core_web_md")

def get_synonyms(word, pos):
    # Use NLTK to get synonyms for a word and a specific part of speech
    synonyms = set()
    try:
        for syn in wordnet.synsets(word, pos=pos):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower())
    except KeyError:
        # Handle the KeyError by using a default part-of-speech tag ('n' for noun)
        for syn in wordnet.synsets(word, pos='n'):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower())

    return list(synonyms)

def replace_with_synonyms(text):
    # Tokenize and tag parts of speech using NLTK
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)

    # Replace words with synonyms
    replaced_text = []
    for token, pos in pos_tags:
        if token.isalpha() and token.lower() not in nltk.corpus.stopwords.words('english'):
            # Get lemmatized word
            lemma = lemmatizer.lemmatize(token.lower(), pos[0].lower())

            # Get synonyms for the lemmatized word and part of speech
            synonyms = get_synonyms(lemma, pos[0].lower())

            if synonyms:
                # Choose a random synonym and append it to the replaced text
                replaced_text.append(random.choice(synonyms))
            else:
                # If no synonyms are found, keep the original word
                replaced_text.append(token)
        else:
            # Keep non-alphabetic and stop words as they are
            replaced_text.append(token)

    return " ".join(replaced_text)

@router.post("/testing/spacy")
async def root(data: RewriteText):
    original_text = data.text
    return {
        "original_text": original_text,
        "rewritten_text": replace_with_synonyms(original_text),
    }



@router.post("/testing/pdf-reader/")
async def upload(file: UploadFile = File(...)):
    # Check if the file is a PDF by verifying the MIME type and file extension
    if file.content_type != "application/pdf" or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        # Generate the full file path for the uploaded file
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

        # Read and save the uploaded PDF file
        contents = file.file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)

        # Convert the PDF to markdown using pymupdf4llm
        markdown_text = pymupdf4llm.to_markdown(file_path)

    except Exception as e:
        return {"message": f"There was an error processing the file: {e}"}
    finally:
        file.file.close()  # Ensure the file is closed after reading

    # Return the markdown text as a response
    return {"message": f"Successfully uploaded {file.filename}", "markdown": markdown_text}