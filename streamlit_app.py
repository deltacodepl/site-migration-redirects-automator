import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def main():
    st.title("Automated Redirect Matchmaker for Site Migrations")

    # Caricamento dei file CSV
    origin_file = st.file_uploader("Upload origin.csv", type="csv")
    destination_file = st.file_uploader("Upload destination.csv", type="csv")

    if origin_file and destination_file:
        origin_df = pd.read_csv(origin_file)
        destination_df = pd.read_csv(destination_file)

        # Identificazione delle colonne comuni
        common_columns = list(set(origin_df.columns) & set(destination_df.columns))
        selected_columns = st.multiselect("Select columns to use for similarity matching:", common_columns)

        if st.button("Match URLs") and selected_columns:
            # Preprocessing dei dati
            origin_df['combined_text'] = origin_df[selected_columns].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
            destination_df['combined_text'] = destination_df[selected_columns].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

            # Matching dei dati
            model = SentenceTransformer('all-MiniLM-L6-v2')
            origin_embeddings = model.encode(origin_df['combined_text'].tolist(), show_progress_bar=False)
            destination_embeddings = model.encode(destination_df['combined_text'].tolist(), show_progress_bar=False)

            dimension = origin_embeddings.shape[1]
            faiss_index = faiss.IndexFlatL2(dimension)
            faiss_index.add(destination_embeddings.astype('float32'))

            distances, indices = faiss_index.search(origin_embeddings.astype('float32'), k=1)
            similarity_scores = 1 - (distances / np.max(distances))

            results_df = pd.DataFrame({
                'origin_url': origin_df['URL'],
                'matched_url': destination_df['URL'].iloc[indices.flatten()],
                'similarity_score': similarity_scores.flatten()
            })

            # Visualizzazione dei risultati
            st.write(results_df)

if __name__ == "__main__":
    main()
