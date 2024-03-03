
# Site Migration Redirects Automator v.1

## Description
This Streamlit tool was developed to automate the process of redirect mapping during website migrations, facilitating the matching of URLs from an old to a new site based on content similarity. Using state-of-the-art natural language processing techniques provided by the `sentence-transformers` library and efficient search algorithms provided by `faiss`, the tool is able to process and compare large datasets, identifying the most relevant matches between the pages of the original site and those of the target site.

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
    
This tool is based on the original Python script [Automated Redirect Matchmaker for Site Migrations](https://colab.research.google.com/drive/1Y4msGtQf44IRzCotz8KMy0oawwZ2yIbT?usp=sharing) developed by [Daniel Emery](https://www.linkedin.com/in/dpe1/), which provides an automated approach to mapping redirects during website migrations.

