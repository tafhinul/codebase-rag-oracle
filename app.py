import streamlit as st
import uuid
import os

# HuggingFace Tokenizer-এর ডেডলক বা হ্যাং হওয়া বন্ধ করার ট্রিক
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="Codebase Oracle", page_icon="🤖")
st.title("🤖 Codebase Oracle AI")
st.markdown("Ask anything about your codebase!")

# ২. Lazy Loading & Caching
@st.cache_resource(show_spinner="⚙️ Initializing AI Model and Vector Database... Please wait.")
def get_initialized_agent():
    from agent import setup_agent 
    return setup_agent()

# ৩. এজেন্ট লোড করা
try:
    agent = get_initialized_agent()
except Exception as e:
    st.error(f"Failed to load the AI Agent. Error: {e}")
    st.stop()

# ৪. সেশন স্টেট (Memory)
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ৫. আগের চ্যাট হিস্ট্রি স্ক্রিনে দেখানো
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ৬. ইউজারের ইনপুট এবং চ্যাট লজিক
user_input = st.chat_input("Ask about your code (e.g., 'What libraries are used for PDFs?')...")

if user_input:
    # ইউজারের মেসেজ UI-তে দেখানো
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # এজেন্টের রেসপন্স
    with st.chat_message("assistant"):
        with st.spinner("Searching the codebase and thinking..."):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            
            try:
                response = agent.invoke({"messages": [("user", user_input)]}, config=config)
                raw_content = response["messages"][-1].content
                
                # --- JSON/List থেকে শুধু Text বের করার লজিক ---
                if isinstance(raw_content, list):
                    # যদি লিস্ট আকারে আসে, তবে শুধু text ভ্যালুগুলো জোড়া লাগাবে
                    bot_reply = "".join([block.get("text", "") for block in raw_content if isinstance(block, dict)])
                else:
                    # যদি প্লেইন টেক্সট হয়, তবে সরাসরি ব্যবহার করবে
                    bot_reply = str(raw_content)
                # ----------------------------------------------
                
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error("The agent encountered an error while processing your request.")
                st.write(e)