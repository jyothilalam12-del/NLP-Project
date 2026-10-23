import streamlit as st

from sentence_transformers import SentenceTransformer


@st.cache_resource
def load_embedding_model():

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    return model


model = load_embedding_model()


def create_embeddings(chunks):

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return embeddings