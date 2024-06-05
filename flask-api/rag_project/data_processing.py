import argparse
import os
import shutil
from pymongo import MongoClient
from langchain.schema.document import Document
from embeddings import embedding_function
from langchain_community.vectorstores.chroma import Chroma

CHROMA_PATH = "chroma"
MONGODB_URL = "mongodb://localhost:27017"
DB_NAME = "Metadata_Cleaned"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="List all stored documents.")
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    parser.add_argument("--id", type=str, help="Retrieve a document by ID.")
    args = parser.parse_args()
    
    if args.list:
        list_documents()
    elif args.id:
        get_document_by_id(args.id)
    elif args.reset:
        clear_database()
    else:
        print("Please provide a valid option. Use --list to list documents, --id to retrieve a document by ID, or --reset to reset the database.")

    documents = load_documents()
    add_to_chroma(documents)

def list_documents():
    client = MongoClient(MONGODB_URL)
    db = client[DB_NAME]

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        print(f"Collection: {collection_name}")
        for doc in collection.find():
            print(doc)
        print()

    client.close()

def get_document_by_id(doc_id):
    embedding_function_instance = embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function_instance)

    document = db.get_document_by_id(doc_id)
    if document:
        print(f"ID: {document.metadata['id']}\nTitle: {document.metadata['title']}\nType: {document.metadata['type']}\nContent: {document.page_content}\nMetadata: {document.metadata}\n")
    else:
        print(f"No document found with ID: {doc_id}")

def load_documents():
    client = MongoClient(MONGODB_URL)
    db = client[DB_NAME]

    documents = []
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        docs = collection.find()
        documents.extend(docs)

    client.close()
    return documents

def add_to_chroma(documents):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function())

    # Create Document instances directly from the loaded documents
    new_documents = [
        Document(page_content=doc["content"], metadata={
            "id": str(doc.get("_id", "")),
            "type": doc.get("type", ""),
            "title": doc.get("title", "")
        }) for doc in documents
    ]

    if new_documents:
        print(f"👉 Adding new documents: {len(new_documents)}")
        new_document_ids = [doc.metadata["id"] for doc in new_documents]
        db.add_documents(new_documents, ids=new_document_ids)
    else:
        print("✅ No new documents to add")

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print(f"✨ Cleared database at {CHROMA_PATH}")
    else:
        print("🔍 No existing database found to clear")

if __name__ == "__main__":
    main()

