import os

from dotenv import load_dotenv
from google import genai


# Load .env
load_dotenv()


# Get API key
api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )


# Gemini client
client = genai.Client(
    api_key=api_key
)


def call_gemini(prompt):

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


def limit_text(
    text,
    max_characters=12000
):

    if len(text) <= max_characters:

        return text

    return text[:max_characters]


def generate_summary(text):

    text = limit_text(text)

    prompt = f"""
You are an AI Study Assistant.

Summarize the following study material.

STUDY MATERIAL:

{text}

Give:

1. Main topics
2. Important points
3. Key definitions
4. Important concepts

Use simple English and bullet points.
"""

    return call_gemini(prompt)


def generate_quiz(
    text,
    number_of_questions=5
):

    text = limit_text(text)

    prompt = f"""
You are an AI Study Assistant.

Create {number_of_questions} multiple-choice
questions from the following study material.

STUDY MATERIAL:

{text}

For each question provide:

Question
A)
B)
C)
D)

Then provide the correct answer.

Do not use information outside the study material.
"""

    return call_gemini(prompt)


def generate_important_questions(text):

    text = limit_text(text)

    prompt = f"""
You are an AI Study Assistant.

Generate important examination questions
from the following study material.

STUDY MATERIAL:

{text}

Provide:

1. Very important questions
2. Short-answer questions
3. Long-answer questions

Focus on concepts likely to be useful for exams.
Use simple English.
"""

    return call_gemini(prompt)