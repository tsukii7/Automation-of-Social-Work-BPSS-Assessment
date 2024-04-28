import pandas as pd
from nltk.tokenize import sent_tokenize
from transformers import pipeline
import json

# Load JSON data
with open('../data/json/conversation_narrative_top3.json', 'r') as file:
    data = json.load(file)

    # Display the structure of the JSON data
    data_structure = {key: type(value) for key, value in data.items()}
    # Convert the JSON data to a DataFrame
    df = pd.DataFrame([(key, val['message_cnt'], val['narrative']) for key, val in data.items() if 'message_cnt' in val],
                      columns=['narrativeID', 'message_cnt', 'narrative'])

    # Tokenize narratives into sentences
    sentences = []
    for idx, row in df.iterrows():
        for sent in sent_tokenize(row['narrative']):
            sentences.append({'narrativeID': row['narrativeID'], 'sentence': sent})

    sentences_df = pd.DataFrame(sentences)

    sentences_df.to_csv('../data/sentences_with_labels.csv', index=False, columns=['narrativeID', 'sentence'])

    sentences_df.head()
