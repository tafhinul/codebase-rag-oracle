import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# আমাদের তৈরি করা ডাটাবেসের পাথ
CHROMA_PATH = "./chroma_db"

def query_codebase(query_text):
    print("Loading embedding model...")
    # ইনজেশনের সময় যে মডেল ব্যবহার করেছি, ঠিক সেটাই এখানে ব্যবহার করতে হবে
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Connecting to Vector Database...")
    # ডাটাবেস লোড করা
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    print(f"\nSearching for: '{query_text}'...\n")
    # similarity_search_with_score ব্যবহার করে সবচেয়ে প্রাসঙ্গিক ৩টি (k=3) রেজাল্ট বের করছি
    results = db.similarity_search_with_score(query_text, k=3)
    
    if not results:
        print("No matching code found in the database.")
        return

    # রেজাল্টগুলো প্রিন্ট করে দেখা
    for i, (doc, score) in enumerate(results):
        # স্কোর যত কম হবে, রেজাল্ট তত ভালো (কারন এটি distance মেজার করে)
        print(f"--- Result {i+1} (Distance Score: {score:.4f}) ---")
        print(f"File Source: {doc.metadata.get('source', 'Unknown File')}")
        print("Code Snippet:")
        print(doc.page_content)
        print("-" * 50 + "\n")

if __name__ == "__main__":
    # এখানে আপনার কোডবেস অনুযায়ী একটি প্রশ্ন লিখুন
    # যেমন, কোডবেসে যদি কোনো meal management রিলেটেড লজিক থাকে, তাহলে কুয়েরি হতে পারে 'How is the daily meal cost calculated?'
    sample_query = "What is the main function for user authentication?" 
    
    query_codebase(sample_query)
