import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def main():
with st.container():
    st.header("Site Migration Redirects Automator v.1")

    st.markdown("""
    **Prima di Utilizzare lo Strumento**

    Per garantire l'efficacia di questo strumento nella mappatura dei redirect, è essenziale preparare adeguatamente i dati di input. Questo processo inizia con l'export dei dati da Screaming Frog, uno strumento di crawling web che fornisce una panoramica dettagliata delle URL esistenti sul tuo sito web.

    **Come Preparare i Dati con Screaming Frog**

    1. Esegui un crawl completo del tuo sito web utilizzando Screaming Frog.
    2. Filtra i risultati del crawl per includere solo le pagine HTML con codice di stato 200, assicurandoti di rimuovere URL duplicati o non necessari per la mappatura dei redirect.
    3. Esporta i risultati filtrati in un file CSV. Assicurati che il file contenga colonne per l'indirizzo URL, il titolo, la descrizione meta e altre informazioni pertinenti che desideri utilizzare per il matching.
    4. Ripeti il processo per il sito web di destinazione, eseguendo un crawl del sito in staging (o del nuovo sito) e esportando i risultati.

    **Scopo e Funzionamento dello Strumento**

    Questo strumento è stato sviluppato per automatizzare il processo di mappatura dei redirect durante le migrazioni dei siti web, facilitando il matching delle URL da un vecchio a un nuovo sito basandosi sulla somiglianza dei contenuti. Utilizzando tecniche all'avanguardia di elaborazione del linguaggio naturale fornite dalla libreria `sentence-transformers` e algoritmi di ricerca efficienti forniti da `faiss`, lo strumento è in grado di processare e confrontare grandi set di dati, identificando le corrispondenze più rilevanti tra le pagine del sito originale e quelle del sito di destinazione.

    **Istruzioni per l'Uso**

    1. Prepara i file CSV contenenti le URL del sito originale (`origin.csv`) e del sito di destinazione (`destination.csv`) seguendo le istruzioni sopra.
    2. Carica i file CSV utilizzando gli appositi uploader.
    3. Seleziona le colonne rilevanti per il matching dal menù a tendina.
    4. Clicca sul pulsante "Match URLs" per avviare il processo di matching.
    5. Visualizza i risultati direttamente nell'interfaccia, che includeranno le URL di origine, le corrispondenti URL di destinazione e i punteggi di somiglianza.
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
