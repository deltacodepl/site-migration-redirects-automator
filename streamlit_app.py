import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def main():
    st.title("Site Migration Redirects Automator v.1")
    st.markdown("""
### Scopo e Funzionamento dello Strumento

Questo strumento è stato sviluppato per automatizzare il processo di mappatura dei redirect durante le migrazioni dei siti web, facilitando il matching delle URL da un vecchio a un nuovo sito basandosi sulla somiglianza dei contenuti. Utilizzando tecniche all'avanguardia di elaborazione del linguaggio naturale fornite dalla libreria `sentence-transformers` e algoritmi di ricerca efficienti forniti da `faiss`, lo strumento è in grado di processare e confrontare grandi set di dati, identificando le corrispondenze più rilevanti tra le pagine del sito originale e quelle del sito di destinazione.

### Istruzioni per l'Uso

1. Carica i file CSV contenenti le URL del sito originale (`origin.csv`) e del sito di destinazione (`destination.csv`) utilizzando gli appositi uploader.
2. Seleziona le colonne rilevanti per il matching dal menù a tendina. Queste colonne possono includere titoli, descrizioni meta, intestazioni e altro contenuto significativo che contribuisce alla somiglianza dei contenuti tra le pagine.
3. Clicca sul pulsante "Match URLs" per avviare il processo di matching.
4. Visualizza i risultati direttamente nell'interfaccia, i quali includeranno le URL di origine, le corrispondenti URL di destinazione e i punteggi di somiglianza, evidenziando così le migliori corrispondenze trovate dall'algoritmo.

Questo strumento è progettato per semplificare e velocizzare una delle fasi più critiche e laboriose delle migrazioni dei siti web, riducendo significativamente il tempo e lo sforzo necessari per eseguire manualmente la mappatura dei redirect.
""")

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

            # Creazione delle serie per gestire lunghezze diverse
            matched_url_series = pd.Series(destination_df['Address'].iloc[indices.flatten()].values, index=origin_df.index)
            similarity_scores_series = pd.Series(similarity_scores.flatten(), index=origin_df.index)

            # Creazione del DataFrame dei risultati
            results_df = pd.DataFrame({
                'origin_url': origin_df['Address'],
                'matched_url': matched_url_series,
                'similarity_score': similarity_scores_series
            })

            # Visualizzazione dei risultati
            st.write(results_df)

if __name__ == "__main__":
    main()
