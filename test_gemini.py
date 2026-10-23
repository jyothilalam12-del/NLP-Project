import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API key found:", api_key is not None)

client = genai.Client(
    api_key=api_key
)

interaction = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input="What is artificial intelligence? Answer in one sentence."
)

print("\nGemini response:")
print(interaction.output_text)