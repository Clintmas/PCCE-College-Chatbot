
import streamlit as st
from src.chatbot import chatbot_reply


# ----------------------------------
# 1. PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="PCCE College Assistant",
    page_icon="🎓",
    layout="wide"
)


# ----------------------------------
# 2. CUSTOM CSS
# ----------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #f4f7fb;
}

.main-title {
    color: #12345a;
    font-size: 32px;
    font-weight: bold;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
}

/* Assistant messages - dark background */
div[data-testid="stChatMessage"]:nth-of-type(odd) {
    background-color: #111827 !important;
    border-radius: 12px;
    padding: 15px;
}

/* Assistant text - white */
div[data-testid="stChatMessage"]:nth-of-type(odd) p,
div[data-testid="stChatMessage"]:nth-of-type(odd) li {
    color: white !important;
}

/* User messages - grey background */
div[data-testid="stChatMessage"]:nth-of-type(even) {
    background-color: #8e9299 !important;
    border-radius: 12px;
    padding: 15px;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid #12345a;
    color: #12345a;
    background-color: white;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #12345a;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------
# 3. SIDEBAR
# ----------------------------------

with st.sidebar:

    st.title("🎓 PCCE")

    st.caption("Padre Conceição College of Engineering")

    st.divider()

    st.subheader("About the College")

    st.write(
        "Welcome to Padre Conceição College of Engineering, "
        "Verna, Goa."
    )

    st.divider()

    st.subheader("College Information")

    st.write("📍 Verna, Goa")

    st.write("📧 agnelpcce@gmail.com")

    st.write("🌐 https://pccegoa.edu.in/")

    st.divider()

    st.subheader("Chat Options")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ----------------------------------
# 4. MAIN HEADING
# ----------------------------------

st.markdown(
    '<div class="main-title">🎓 PCCE College Enquiry Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your virtual assistant for college-related enquiries.</div>',
    unsafe_allow_html=True
)

st.divider()


# ----------------------------------
# 5. INITIALIZE CHAT HISTORY
# ----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Welcome screen

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div style="text-align:center; padding:30px 10px;">
            <h1 style="color:#12345a;">🎓 Welcome to PCCE!</h1>
            <h3 style="color:#64748b;">
                Your College Enquiry Assistant
            </h3>
            <p style="color:#64748b; font-size:17px;">
                Get quick answers about courses, admissions,
                fees, placements and college facilities.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ADD SUGGESTED QUESTIONS HERE

    st.markdown("### 💡 Not sure what to ask?")

    suggestions = [
        "What courses are available?",
        "What are the college fees?",
        "How can I apply for admission?",
        "Is hostel available?"
    ]

    for question in suggestions:
        if st.button(question, use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            response = chatbot_reply(question)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()

# ----------------------------------
# 6. QUICK ENQUIRY BUTTONS
# ----------------------------------

st.subheader("Quick Enquiries")

col1, col2, col3 = st.columns(3)

quick_question = None

with col1:
    if st.button("📚 Courses"):
        quick_question = "What courses are available?"

with col2:
    if st.button("💰 Fees"):
        quick_question = "What are the college fees?"

with col3:
    if st.button("📝 Admissions"):
        quick_question = "How can I apply for admission?"

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("🏠 Hostel"):
        quick_question = "Is hostel available?"

with col5:
    if st.button("🚌 Transport"):
        quick_question = "Do you provide transport?"

with col6:
    if st.button("📍 Location"):
        quick_question = "Where is the college located?"


# ----------------------------------
# 7. DISPLAY CHAT HISTORY
# ----------------------------------

st.markdown("---")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

st.markdown("---")


# ----------------------------------
# 8. PROCESS USER QUESTION
# ----------------------------------

user_input = st.chat_input(
    "💬 Ask me anything about PCCE..."
)

if quick_question:

    user_input = quick_question


if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("🤖 PCCE Assistant is thinking..."):
        response = chatbot_reply(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
    

    st.rerun()
