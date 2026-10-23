🎓 AI Study Assistant

📌 Introduction
The AI Study Assistant is an AI-powered application designed to help students learn more effectively and save time. It allows students to interact with AI, ask questions about PDF documents, summarize study materials, generate quizzes, and prepare important questions for exams.
The application uses Natural Language Processing (NLP), document processing, and Retrieval-Augmented Generation (RAG) to provide relevant answers based on uploaded study materials.

✨ Features
- AI Chat: Ask questions and receive AI-generated answers.
- Ask from PDF: Upload PDF documents and ask questions about their content.
- Text Summarization: Generate concise summaries of study materials.
- Quiz Generation: Create quizzes to test your knowledge.
- Important Questions: Generate important questions from study materials.
- User-Friendly Interface: Simple and interactive interface built with Streamlit.

🛠️ Technologies Used
- Python: Main programming language.
- Streamlit: Creates the interactive web application.
- Gemini API: Generates AI-powered responses.
- Sentence Transformers: Converts text into numerical embeddings.
- FAISS: Searches for relevant document sections efficiently.
- PyPDF: Extracts text from PDF documents.
- RAG (Retrieval-Augmented Generation): Retrieves relevant information from uploaded documents to help generate answers.

⚙️ Installation and Setup

1. Clone the Repository

git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git

2. Open the Project Folder

cd AI_Study_Assistant

3. Create a Virtual Environment

python -m venv .venv

4. Activate the Virtual Environment

For Windows:

.venv\Scripts\activate

5. Install Dependencies

If a "requirements.txt" file is included:

pip install -r requirements.txt

6. Configure the Gemini API Key

Create a ".env" file in the project directory and add your Gemini API key using the environment variable name expected by your application.

Important: Never upload your API key or ".env" file to GitHub.

7. Run the Application

streamlit run app.py

The application will open in your browser.

🎯 Project Objectives
- Help students understand study materials efficiently.
- Reduce the time required to summarize lengthy documents.
- Support interactive learning through AI-generated quizzes.
- Make it easier to find answers within PDF study materials.
- Improve exam preparation through automatically generated questions.

🚀 Future Enhancements
- Support additional document formats.
- Add user authentication and personalized learning.
- Maintain learning history and progress.
- Improve answer accuracy and response speed.
- Add multilingual learning support.

