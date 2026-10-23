
import streamlit as st

from utils.pdf_processor import (
    extract_text_from_pdf,
    split_text
)
from utils.embeddings import create_embeddings
from utils.vector_db import create_vector_database
from utils.rag import ask_question
from utils.study_features import (
    generate_summary,
    generate_quiz,
    generate_important_questions
)



# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# FEATURE NAVIGATION STATE
# --------------------------------------------------

FEATURES = [
    "🏠 Home",
    "💬 AI Chat",
    "📄 Ask from PDF",
    "📝 Summarize",
    "❓ Generate Quiz",
    "⭐ Important Questions"
]

if "selected_feature" not in st.session_state:
    st.session_state.selected_feature = "🏠 Home"

if "sidebar_feature" not in st.session_state:
    st.session_state.sidebar_feature = "🏠 Home"


def update_feature_from_sidebar():
    st.session_state.selected_feature = (
        st.session_state.sidebar_feature
    )


# Process a card click BEFORE the sidebar radio is created.
# This avoids StreamlitWidgetAlreadyInstantiatedError.

if "pending_feature" in st.session_state:
    pending = st.session_state.pending_feature

    st.session_state.selected_feature = pending
    st.session_state.sidebar_feature = pending

    del st.session_state.pending_feature


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main page background */
.stApp {
    background: linear-gradient(
        135deg,
        #f5f3ff 0%,
        #eff6ff 50%,
        #ecfeff 100%
    ) !important;
    color: #1e293b !important;
}

/* Fix the top header */
[data-testid="stHeader"] {
    background: linear-gradient(
        90deg,
        #ede9fe,
        #dbeafe,
        #cffafe
    ) !important;
}

/* Toolbar */
[data-testid="stToolbar"] {
    background: transparent !important;
}

/* Main page spacing */
.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #e0e7ff,
        #f5f3ff,
        #cffafe
    ) !important;
    border-right: 1px solid #c7d2fe;
}

/* Sidebar text */
[data-testid="stSidebar"],
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong {
    color: #1e293b !important;
}

/* Sidebar captions */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #475569 !important;
}

/* Sidebar radio labels */
[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [role="radiogroup"] label p,
[data-testid="stSidebar"] [role="radiogroup"] label span {
    color: #1e293b !important;
}

/* Selected sidebar radio option */
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    color: #3730a3 !important;
    font-weight: 600;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: #c7d2fe;
}

/* Sidebar icons */
[data-testid="stSidebar"] svg {
    color: #4338ca;
}

/* Main headings */
h1, h2, h3 {
    color: #3730a3;
}

/* Hero banner */
.hero {
    background: linear-gradient(
        110deg,
        #4f46e5,
        #8b5cf6,
        #06b6d4
    );
    padding: 30px;
    border-radius: 22px;
    color: #ffffff;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.20);
}

.hero h1 {
    color: #ffffff !important;
    font-size: 36px;
    margin: 0;
}

.hero p {
    color: #ffffff !important;
    font-size: 17px;
    margin-top: 10px;
}

/* All feature cards have the same size */
.feature-card {
    box-sizing: border-box;
    width: 100%;
    height: 145px;
    padding: 18px;
    border-radius: 17px;
    margin-bottom: 12px;
    border: 1px solid rgba(129, 140, 248, 0.25);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.06);

    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    overflow: hidden;
}

.feature-card h3 {
    color: #3730a3 !important;
    font-size: 18px;
    margin: 0 0 8px 0;
    line-height: 1.4;
}

.feature-card p {
    color: #475569 !important;
    font-size: 14px;
    margin: 0;
    line-height: 1.4;
}

/* Keep all feature buttons the same height */
.stButton > button {
    min-height: 43px;
    width: 100%;
}

/* Mobile layout */
@media (max-width: 768px) {
    .feature-card {
        height: 145px;
    }
}
/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    ) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 11px;
    min-height: 43px;
    font-weight: 650;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(
        90deg,
        #4f46e5,
        #7c3aed
    ) !important;
    color: #ffffff !important;
    border: none !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 14px rgba(99, 102, 241, 0.25);
}

/* Text inputs */
.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    border: 1px solid #c4b5fd !important;
    border-radius: 10px;
    color: #1e293b !important;
}

/* Input labels */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stFileUploader label {
    color: #1e293b !important;
}

/* Select box */
[data-testid="stSelectbox"] {
    border-radius: 10px;
}

[data-testid="stSelectbox"] * {
    color: #1e293b;
}

/* PDF uploader background */
[data-testid="stFileUploader"] {
    background: #eff6ff !important;
    border: 2px dashed #6366f1 !important;
    border-radius: 16px;
    padding: 15px;
}

/* PDF uploader text */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] {
    color: #1e293b !important;
}

/* File uploader drop zone */
[data-testid="stFileUploaderDropzone"] {
    background: #f8fafc !important;
    border: 1px dashed #a5b4fc !important;
    border-radius: 12px !important;
}

/* Browse files button */
[data-testid="stFileUploader"] button {
    background: #4f46e5 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploader"] button span,
[data-testid="stFileUploader"] button p {
    color: #ffffff !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Result cards */
.result-card {
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid #ddd6fe;
    border-radius: 16px;
    padding: 20px;
    margin-top: 12px;
    box-shadow: 0 5px 18px rgba(79, 70, 229, 0.08);
    color: #1e293b;
    overflow-wrap: anywhere;
}

.result-card h3 {
    color: #3730a3 !important;
}

.result-card p {
    color: #475569 !important;
}

/* Footer */
.footer {
    background: linear-gradient(
        90deg,
        #8b5cf6,
        #6366f1,
        #06b6d4
    );
    color: #ffffff;
    padding: 17px;
    text-align: center;
    border-radius: 15px;
    margin-top: 30px;
    font-weight: 600;
}

.footer span {
    color: #ffffff !important;
}

/* Mobile layout */
@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem;
    }

    .hero {
        padding: 20px;
    }

    .hero h1 {
        font-size: 27px;
    }

    .feature-card {
        min-height: auto;
    }
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HERO BANNER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>🎓 AI Study Assistant</h1>
    <p>Learn Smarter • Study Better • Achieve More ✨</p>
    <p>
        Your personal AI learning partner powered by Gemini.
        Upload your notes, ask questions, create summaries and practise quizzes.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 📚 Study Features")
    st.caption("Choose your learning activity")

    st.radio(
        "Navigate",
        FEATURES,
        key="sidebar_feature",
        on_change=update_feature_from_sidebar,
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 🌟 Your Study Partner")
    st.write("📖 Learn at your own pace.")
    st.write("🧠 Understand difficult concepts.")
    st.write("🚀 Prepare for exams.")

    st.caption("Powered by Gemini • NLP • FAISS")


# Use the current selected feature after the radio renders.
feature = st.session_state.selected_feature


# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

columns = st.columns(5)

cards = [
    ("💬 AI Chat", "Ask general questions.", "card-blue"),
    ("📄 Ask from PDF", "Explore your uploaded notes.", "card-purple"),
    ("📝 Summarize", "Revise key concepts.", "card-green"),
    ("❓ Generate Quiz", "Practise with questions.", "card-orange"),
    ("⭐ Important Questions", "Prepare for examinations.", "card-pink")
]

for column, (title, description, style) in zip(columns, cards):

    with column:

        st.markdown(
            f"""
            <div class="feature-card {style}">
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Navigate directly when the user clicks a card button.
        if st.button(
            f"Open {title}",
            key=f"open_feature_{title}",
            use_container_width=True
        ):
            st.session_state.pending_feature = title
            st.rerun()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "pdf_text": None,
    "chunks": None,
    "index": None,
    "file_name": None,
    "last_answer": None,
    "last_summary": None,
    "last_quiz": None,
    "last_important": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# PDF UPLOAD
# --------------------------------------------------

st.markdown("## 📂 Upload Your Study Material")

uploaded_file = st.file_uploader(
    "Choose a PDF file containing your notes or textbook",
    type=["pdf"],
    help="Upload a text-based PDF to use the study tools."
)


# --------------------------------------------------
# PROCESS PDF
# --------------------------------------------------

if uploaded_file is not None:

    if st.session_state.file_name != uploaded_file.name:

        # Clear previous document data.
        st.session_state.pdf_text = None
        st.session_state.chunks = None
        st.session_state.index = None
        st.session_state.file_name = None

        st.session_state.last_answer = None
        st.session_state.last_summary = None
        st.session_state.last_quiz = None
        st.session_state.last_important = None

        try:
            with st.spinner("✨ Processing your PDF..."):

                text = extract_text_from_pdf(uploaded_file)

                if not text or not text.strip():
                    st.error(
                        "No text was extracted. "
                        "This PDF may contain scanned images."
                    )
                    st.stop()

                chunks = split_text(
                    text,
                    chunk_size=1000,
                    overlap=100
                )

                embeddings = create_embeddings(chunks)
                index = create_vector_database(embeddings)

                st.session_state.pdf_text = text
                st.session_state.chunks = chunks
                st.session_state.index = index
                st.session_state.file_name = uploaded_file.name

            st.success("✅ PDF processed successfully!")

        except Exception as e:
            st.error(f"Unable to process the PDF: {e}")
            st.stop()

    else:
        st.success(f"📘 Ready to study: {uploaded_file.name}")

else:

    # Clear document data if the upload is removed.
    if st.session_state.file_name is not None:

        st.session_state.pdf_text = None
        st.session_state.chunks = None
        st.session_state.index = None
        st.session_state.file_name = None

        st.session_state.last_answer = None
        st.session_state.last_summary = None
        st.session_state.last_quiz = None
        st.session_state.last_important = None

    st.info("👆 Upload a PDF to enable your study tools.")


# --------------------------------------------------
# HOME
# --------------------------------------------------

if feature == "🏠 Home":

    st.markdown("## 🌈 Welcome to Your Learning Space")

    left, right = st.columns(2)

    with left:
        st.markdown("""
        <div class="result-card">
            <h3>📚 Study smarter</h3>
            <p>Upload your study material and get started.</p>
            <p>✨ Generate summaries and important questions.</p>
            <p>🧩 Test your knowledge with quizzes.</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="result-card">
            <h3>🤖 Your AI assistant</h3>
            <p>Ask questions about your notes.</p>
            <p>💡 Get clear explanations in simple English.</p>
            <p>🚀 Use AI Chat for general questions too.</p>
        </div>
        """, unsafe_allow_html=True)


# --------------------------------------------------
# AI CHAT
# --------------------------------------------------

elif feature == "💬 AI Chat":

    st.markdown("## 💬 AI Chat")
    st.write("Ask questions about your notes or general topics.")

    if st.session_state.pdf_text is None:

        st.info("Upload a PDF above to enable AI Chat.")

    else:

        with st.form("ai_chat_form"):

            question = st.text_input(
                "What would you like to learn?",
                placeholder="Example: What is machine learning?"
            )

            submitted = st.form_submit_button("✨ Ask Gemini")

        if submitted:

            if question.strip():

                with st.spinner("🤖 Thinking..."):

                    try:
                        answer = ask_question(
                            question,
                            st.session_state.index,
                            st.session_state.chunks
                        )

                        st.session_state.last_answer = answer

                    except Exception as e:
                        st.error(f"Unable to generate an answer: {e}")

            else:
                st.warning("Please enter a question.")

        if st.session_state.last_answer:

            st.markdown("### 🌟 Answer")

            st.markdown(
                f'<div class="result-card">'
                f'{st.session_state.last_answer}'
                f'</div>',
                unsafe_allow_html=True
            )


# --------------------------------------------------
# ASK FROM PDF
# --------------------------------------------------

elif feature == "📄 Ask from PDF":

    st.markdown("## 📄 Ask Questions from Your PDF")

    if st.session_state.pdf_text is None:

        st.info("Please upload a PDF first.")

    else:

        with st.form("pdf_question_form"):

            question = st.text_input(
                "Ask something from your uploaded notes:",
                placeholder="Example: Explain the main concepts."
            )

            submitted = st.form_submit_button("🔎 Search My Notes")

        if submitted:

            if question.strip():

                with st.spinner("📚 Searching your study material..."):

                    try:
                        answer = ask_question(
                            question,
                            st.session_state.index,
                            st.session_state.chunks
                        )

                        st.session_state.last_answer = answer

                    except Exception as e:
                        st.error(f"Unable to search your PDF: {e}")

            else:
                st.warning("Please enter a question.")

        if st.session_state.last_answer:

            st.markdown("### 📖 Answer")

            st.markdown(
                f'<div class="result-card">'
                f'{st.session_state.last_answer}'
                f'</div>',
                unsafe_allow_html=True
            )


# --------------------------------------------------
# SUMMARIZE
# --------------------------------------------------

elif feature == "📝 Summarize":

    st.markdown("## 📝 Summarize Study Material")

    st.write(
        "Turn your uploaded notes into an easy-to-revise summary."
    )

    if st.session_state.pdf_text is None:

        st.info("Please upload a PDF first.")

    elif st.button("✨ Generate Summary"):

        with st.spinner("📝 Creating your summary..."):

            try:
                st.session_state.last_summary = generate_summary(
                    st.session_state.pdf_text
                )

            except Exception as e:
                st.error(f"Unable to generate summary: {e}")

    if st.session_state.last_summary:

        st.markdown("### 📚 Your Summary")

        st.markdown(
            f'<div class="result-card">'
            f'{st.session_state.last_summary}'
            f'</div>',
            unsafe_allow_html=True
        )


# --------------------------------------------------
# GENERATE QUIZ
# --------------------------------------------------

elif feature == "❓ Generate Quiz":

    st.markdown("## ❓ Test Your Knowledge")

    st.write(
        "Generate multiple-choice questions from your study material."
    )

    if st.session_state.pdf_text is None:

        st.info("Please upload a PDF first.")

    else:

        number_of_questions = st.selectbox(
            "Number of questions",
            [5, 10, 15]
        )

        if st.button("🎯 Generate Quiz"):

            with st.spinner("🧠 Preparing your quiz..."):

                try:
                    st.session_state.last_quiz = generate_quiz(
                        st.session_state.pdf_text,
                        number_of_questions
                    )

                except Exception as e:
                    st.error(f"Unable to generate quiz: {e}")

        if st.session_state.last_quiz:

            st.markdown("### 📝 Your Quiz")

            st.markdown(st.session_state.last_quiz)


# --------------------------------------------------
# IMPORTANT QUESTIONS
# --------------------------------------------------

elif feature == "⭐ Important Questions":

    st.markdown("## ⭐ Important Examination Questions")

    st.write(
        "Prepare for your exams using questions from your notes."
    )

    if st.session_state.pdf_text is None:

        st.info("Please upload a PDF first.")

    elif st.button("✨ Generate Important Questions"):

        with st.spinner("📖 Analysing your study material..."):

            try:
                st.session_state.last_important = (
                    generate_important_questions(
                        st.session_state.pdf_text
                    )
                )

            except Exception as e:
                st.error(f"Unable to generate questions: {e}")

    if st.session_state.last_important:

        st.markdown("### 📚 Questions for Revision")

        st.markdown(st.session_state.last_important)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    📚 Learn &nbsp; • &nbsp; Practice &nbsp; • &nbsp; Grow 🌱
    <br>
    <span style="font-size:13px; font-weight:400;">
        AI Study Assistant | Powered by Gemini
    </span>
</div>
""", unsafe_allow_html=True)

