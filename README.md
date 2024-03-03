
# Site Migration Redirects Automator v.1

## Description
This Streamlit application automates the creation of redirect mappings for site migrations by leveraging content similarity analysis between source and destination URLs. It uses advanced natural language processing techniques and search algorithms to identify the best possible matches.

## Features
- Upload CSV files for source and destination URLs
- Automatically calculate content similarity between URLs
- Display recommended redirect mappings with similarity scores

## How to Use
1. Install all dependencies from `requirements.txt`.
2. Start the application with Streamlit using the command `streamlit run streamlit_app.py`.
3. Upload the source and destination CSV files through the user interface.
4. Click on "Run Matching" to generate the redirect mappings.

## Technologies Used
- Streamlit
- Pandas
- Sentence Transformers
- FAISS (Facebook AI Similarity Search)

## Installation
To install the necessary dependencies, run:
```bash
pip install -r requirements.txt
```

## Credits
    
Questo strumento si basa sullo script Python originale [Automated Redirect Matchmaker for Site Migrations](https://colab.research.google.com/drive/1Y4msGtQf44IRzCotz8KMy0oawwZ2yIbT?usp=sharing) sviluppato da [Daniel Emery](https://www.linkedin.com/in/dpe1/), che fornisce un approccio automatizzato alla mappatura dei redirect durante le migrazioni dei siti web.

