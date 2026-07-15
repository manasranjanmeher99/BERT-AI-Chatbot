import streamlit as st
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------

st.set_page_config(
    page_title="BERT AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------------

st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
}

/* Background */
.stApp{
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 35%,
        #312e81 70%,
        #4f46e5 100%
    );
}

/* Main Container */
.main > div{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(18px);
    padding:30px;
    border-radius:20px;
    box-shadow:0 10px 35px rgba(0,0,0,.35);
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:rgba(15,23,42,.85);
    border-right:1px solid rgba(255,255,255,.08);
}

/* Sidebar Text */
section[data-testid="stSidebar"] *{
    color:white;
}

/* Headings */
h1,h2,h3,h4{
    color:white !important;
}

/* Paragraphs */
p,label{
    color:#e2e8f0 !important;
}

/* Text Input */
.stTextInput input{
    border-radius:12px !important;
    border:1px solid rgba(255,255,255,.25);
    background:rgba(255,255,255,.08);
    color:white;
}

/* Buttons */
.stButton>button{
    border-radius:12px;
    background:#4f46e5;
    color:white;
    border:none;
    font-weight:bold;
    transition:.3s;
}

.stButton>button:hover{
    background:#6366f1;
    transform:scale(1.03);
}

/* Chat Messages */
div[data-testid="stChatMessage"]{
    border-radius:18px;
    background:rgba(255,255,255,.08);
    padding:12px;
    margin-bottom:12px;
}

/* Footer */
footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# LOAD BERT MODEL
# -------------------------------------------------------

@st.cache_resource
def load_bert_model():

    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    model = BertModel.from_pretrained("bert-base-uncased")

    return tokenizer, model


tokenizer, model = load_bert_model()

# -------------------------------------------------------
# QUESTIONS & ANSWERS
# -------------------------------------------------------

qa_pairs = {

    "what is your name?":
        "I am a chatbot powered by Google's BERT model.",

    "how are you?":
        "I'm doing great! Thanks for asking.",

    "what is bert?":
        "BERT stands for Bidirectional Encoder Representations from Transformers. It is a deep learning model developed by Google for Natural Language Processing.",

    "tell me a joke.":
        "Why don't programmers like nature? It has too many bugs.",

    "what is ai":
        "Artificial Intelligence (AI) is the ability of machines to simulate human intelligence such as learning, reasoning, problem-solving, and decision-making.",

    "what is data science":
        "Data Science combines statistics, programming, and domain knowledge to analyze data and extract meaningful insights.",

    "what is microsoft azure":
        "Microsoft Azure is Microsoft's cloud computing platform that provides services such as virtual machines, AI, databases, analytics, storage, and networking.",

    "what is your use":
        "I answer questions using BERT embeddings and cosine similarity to understand the meaning of your query."
}

# -------------------------------------------------------
# EMBEDDING FUNCTION
# -------------------------------------------------------

def get_bert_embedding(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    return outputs.last_hidden_state.mean(dim=1).numpy()

# -------------------------------------------------------
# PRECOMPUTE EMBEDDINGS
# -------------------------------------------------------

predefined_embeddings = {
    question: get_bert_embedding(question)
    for question in qa_pairs
}

# -------------------------------------------------------
# CHATBOT RESPONSE
# -------------------------------------------------------

def chatbot_response(user_input):

    user_input = user_input.lower().strip()

    user_embedding = get_bert_embedding(user_input)

    similarities = {

        question: cosine_similarity(
            user_embedding,
            predefined_embeddings[question]
        )[0][0]

        for question in qa_pairs

    }

    best_match = max(similarities, key=similarities.get)

    if similarities[best_match] >= 0.70:
        return qa_pairs[best_match]

    return "Sorry, I couldn't understand your question. Please try asking something else."

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

with st.sidebar:

    st.markdown("## 🤖 BERT AI Chatbot")

    st.markdown("---")

    st.write("### 🚀 Features")

    st.markdown("""
    - 💬 Semantic Question Answering
    - 🧠 BERT Embeddings
    - 📏 Cosine Similarity
    - ⚡ Streamlit Interface
    - 🔍 Fast Response
    """)

    st.markdown("---")

    st.write("### 📚 Supported Topics")

    st.markdown("""
    ✔ Artificial Intelligence

    ✔ Data Science

    ✔ Microsoft Azure

    ✔ BERT

    ✔ General Knowledge
    """)

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.markdown(
"""
# 🤖 BERT AI Chatbot

### Your Intelligent AI Assistant

Ask me anything about **Artificial Intelligence**, **Data Science**, **BERT**, or **Microsoft Azure**.
"""
)

st.markdown("---")


# -------------------------------------------------------
# CHAT HISTORY
# -------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------------------------------------
# DISPLAY OLD MESSAGES
# -------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -------------------------------------------------------
# CHAT INPUT
# -------------------------------------------------------

prompt = st.chat_input("💬 Type your question here...")


# -------------------------------------------------------
# PROCESS USER INPUT
# -------------------------------------------------------

if prompt:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    response = chatbot_response(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# -------------------------------------------------------
# WELCOME MESSAGE
# -------------------------------------------------------

if len(st.session_state.messages) == 0:

    st.info(
        """
### 👋 Welcome!

You can ask questions like:

• What is AI?

• What is BERT?

• What is Data Science?

• Tell me a joke.

• What is Microsoft Azure?

Start typing below 👇
"""
    )


# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------

st.markdown("---")

st.markdown(
"""
<div style='text-align:center;
padding:10px;
color:#CBD5E1;'>

Built with ❤️ using

<b>Streamlit</b> |
<b>PyTorch</b> |
<b>Transformers</b> |
<b>BERT</b>

</div>
""",
unsafe_allow_html=True
)