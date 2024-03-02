
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def load_data(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return None

def main():
    st.title("Automated Redirect Matchmaker for Site Migrations")

    st.subheader("Carica i file CSV")
    origin_file = st.file_uploader("Carica il file CSV di origine", type="csv")
    destination_file = st.file_uploader("Carica il file CSV di destinazione", type="csv")

    if origin_file and destination_file:
        origin_df = load_data(origin_file)
        destination_df = load_data(destination_file)

        if st.button("Esegui Matching"):
            origin_df['combined_text'] = origin_df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
            destination_df['combined_text'] = destination_df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

            model = SentenceTransformer('all-MiniLM-L6-v2')
            origin_embeddings = model.encode(origin_df['combined_text'].tolist(), show_progress_bar=False)
            destination_embeddings = model.encode(destination_df['combined_text'].tolist(), show_progress_bar=False)

            dimension = origin_embeddings.shape[1]
            faiss_index = faiss.IndexFlatL2(dimension)
            faiss_index.add(np.array(destination_embeddings).astype('float32'))

            distances, indices = faiss_index.search(np.array(origin_embeddings).astype('float32'), k=1)

            results_df = pd.DataFrame({
                'URL Origine': origin_df['combined_text'],
                'URL Corrispondente': destination_df['combined_text'].iloc[indices.flatten()],
                'Score di Somiglianza': 1 - (distances.flatten() / np.max(distances))
            })

            st.write(results_df)

if __name__ == "__main__":
    main()
