# Hacking Book Chatbot

A context-aware, book-trained chatbot built using cutting-edge NLP techniques. This project utilizes natural language processing to provide intelligent and relevant answers from a curated collection of hacking and cybersecurity books sourced from [tanc7/hacking-books](https://github.com/tanc7/hacking-books).

## Dataset

This chatbot is trained on a selection of hacking and cybersecurity books. The original corpus is sourced from:

- [https://github.com/tanc7/hacking-books](https://github.com/tanc7/hacking-books)

Books were preprocessed, cleaned, chunked, and embedded to enable semantic search and context-aware interactions.

## Features

- Fast, intelligent question answering over book content  
- Semantic similarity via sentence embeddings  
- Chunked context retrieval from large documents  
- Interactive querying of technical content in cybersecurity, ethical hacking, reverse engineering, and more  

## Tech Stack

- **Language Model**: Gemini / HuggingFace Transformers  
- **Embedding Model**: SentenceTransformers (e.g., `all-MiniLM-L6-v2`)  
- **Vector Store**: Pinecone  
- **Backend**: Python  
- **Interface**: CLI (Streamlit optional for GUI)

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Satyajeet-Pani/AI-ML.git
cd AI-ML/Chatbot
```
### 2. Install required packages

```bash
pip install -r requirements.txt
```

### 3. Put your API Keys in the .env file

Pinecone API Key and Gemini API Key required. Create one.

### 4. Run store_index.py once

## Usage

Run the app.py file and ask any questions related to cybersecurity 
