import faiss
import numpy as np


def create_vector_database(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(
        np.array(embeddings).astype("float32")
    )

    return index


def search_similar_chunks(
    index,
    query_embedding,
    chunks,
    k=2
):

    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"),
        k
    )

    results = []

    for index_value in indices[0]:

        if index_value < len(chunks):

            results.append(
                chunks[index_value]
            )

    return results