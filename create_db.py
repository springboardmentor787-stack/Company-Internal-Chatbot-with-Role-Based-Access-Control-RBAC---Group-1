# create_db.py

from document_loader.chroma_store import create_chroma_db
import os

if __name__ == "__main__":
    print("Checking for existing chroma_db...")

    if os.path.exists("chroma_db"):
        print("chroma_db already exists. Delete it manually if you want to recreate.")
    else:
        print("Creating Chroma DB...")
        create_chroma_db()
        print("Chroma DB created successfully.")