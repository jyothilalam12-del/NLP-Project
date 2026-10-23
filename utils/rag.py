import os

from dotenv import load_dotenv
from google import genai

from utils.embeddings import model
from utils.vector_db import search_similar_chunks


# Load .env
load_dotenv()


# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )


# Create Gemini client
client = genai.Client(
    api_key=api_key
)


def ask_question(question, index, chunks):

    # Create embedding for the question
    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        show_progress_bar=False
    )

    # Search relevant PDF chunks
    relevant_chunks = search_similar_chunks(
        index,
        question_embedding[0],
        chunks,
        k=2
    )

    # Combine relevant chunks
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an AI Study Assistant.

The student has uploaded study material.

You have two sources of information:

1. Uploaded study material
2. Your general knowledge

Rules:

1. If the question is related to the uploaded
study material, use the study material.

2. If the question is not related to the uploaded
study material, answer using your general knowledge.

3. If the answer is based on general knowledge,
say:
"This answer is based on general knowledge."

4. Explain in simple English.

5. Do not claim that information came from the
PDF if it did not.

UPLOADED STUDY MATERIAL:

{context}

STUDENT QUESTION:

{question}

ANSWER:
"""

    try:

        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt
        )

        if interaction.output_text:
            return interaction.output_text.strip()

        return "Gemini did not return an answer."

    except Exception as e:

        return f"Gemini Error: {e}"