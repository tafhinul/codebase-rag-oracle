import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import create_retriever_tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

# .env ফাইল লোড করা এবং এনভ ভ্যারিয়েবল সেট করা
load_dotenv()

CHROMA_PATH = "./chroma_db"

def setup_agent():
    print("Loading database and tools...")
    # ১. ডাটাবেস লোড করা (আপনার আগের তৈরি করা ডাটাবেস)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # ২. ডাটাবেসকে রিট্রিভার বানানো
    retriever = db.as_retriever(search_kwargs={"k": 3})
    
    # ৩. রিট্রিভারকে একটি 'Tool' হিসেবে কনভার্ট করা
    codebase_search_tool = create_retriever_tool(
        retriever,
        "search_codebase",
        "Searches and returns code snippets from the codebase. Always use this tool when the user asks anything about the code, functions, passwords, or logic."
    )
    
    tools = [codebase_search_tool]

    # ৪. LLM সেটআপ (Gemini 1.5 Flash ব্যবহার করছি, যা Tool Calling-এর জন্য বেশ ফাস্ট)
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)

    # ৫. এজেন্টের জন্য প্রম্পট তৈরি (System Message)
    system_prompt = "You are an expert Software Engineering Assistant. Use the provided codebase search tool to answer questions about the user's code. Explain the code clearly in a beginner-friendly way. If the answer is not in the codebase, say you don't know."

    # ৬. রিঅ্যাক্ট এজেন্ট তৈরি (LangGraph)
    agent_executor = create_react_agent(llm, tools, prompt=system_prompt) 
    
    return agent_executor

if __name__ == "__main__":
    agent = setup_agent()
    
    print("\n--- Codebase Oracle Initialized ---")
    
    # আপনার আগের রিট্রিভাল টেস্টের উপর ভিত্তি করে একটি প্রশ্ন সেট করলাম
    user_query = "What modules or libraries are used for handling passwords and PDFs in this codebase? Explain briefly how they work."
    
    print(f"\nUser Query: {user_query}\n")
    
    # এজেন্টকে কল করা হচ্ছে
    response = agent.invoke({"messages": [("user", user_query)]})
    
    print("\n" + "="*50)
    print("--- Final Answer from Agent ---")
    print("="*50)
    print(response["messages"][-1].content)