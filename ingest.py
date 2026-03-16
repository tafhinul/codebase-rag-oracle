import os
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma





# কনফিগারেশন
REPO_PATH = "./codebase_to_scan"  # আপনার কোডবেসের পাথ
CHROMA_PATH = "./chroma_db"       # যেখানে ডাটাবেস সেভ হবে

def load_and_chunk_codebase(repo_path):
    print(f"Loading files from: {repo_path}...")
    
    # GenericLoader এবং LanguageParser ব্যবহার করে শুধু Python ফাইল লোড করছি
    # আপনি চাইলে Language.JS বা অন্যান্য ভাষাও অ্যাড করতে পারেন
    loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=[".py"], # আপাতত শুধু পাইথন ফাইল নিচ্ছি
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=50),
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} Python files.")

    # কোডের সিনট্যাক্স অনুযায়ী চাঙ্ক করার জন্য RecursiveCharacterTextSplitter
    # এটি চেষ্টা করবে ফাংশন বা ক্লাসগুলোকে না ভেঙে একসাথে রাখতে
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, 
        chunk_size=1000, 
        chunk_overlap=200
    )
    
    chunks = python_splitter.split_documents(documents)
    print(f"Split codebase into {len(chunks)} chunks.")
    
    return chunks

def create_vector_db(chunks, persist_directory):
    print("Initializing HuggingFace Embeddings (Local)...")
    # লোকালি রান করার জন্য sentence-transformers ব্যবহার করছি
    # এটি ডিপ লার্নিং মডেল ব্যবহার করে টেক্সটকে ভেক্টরে কনভার্ট করবে
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Saving to Chroma Vector Database...")
    db = Chroma.from_documents(
        chunks, 
        embeddings, 
        persist_directory=persist_directory
    )
    print(f"Database successfully saved at: {persist_directory}")
    return db

if __name__ == "__main__":
    if not os.path.exists(REPO_PATH):
        print(f"Error: {REPO_PATH} ফোল্ডারটি পাওয়া যায়নি। দয়া করে ফোল্ডারটি তৈরি করে কিছু কোড রাখুন।")
    else:
        # ১. কোড লোড এবং চাঙ্ক করা
        code_chunks = load_and_chunk_codebase(REPO_PATH)
        
        # ২. ভেক্টর ডাটাবেস তৈরি এবং সেভ করা
        if len(code_chunks) > 0:
            create_vector_db(code_chunks, CHROMA_PATH)
        else:
            print("No chunks found to process.")