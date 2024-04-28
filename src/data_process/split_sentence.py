import pandas as pd
from datasets import load_dataset
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

dataset = load_dataset( "nbertagnolli/counsel-chat" )
df = pd.DataFrame(dataset['train'])
df = df.drop_duplicates(subset=['questionID'])

sentences_data = []

for index, row in df.iterrows():
    question_text = row['questionText']
    if isinstance(question_text, str):
        sentences = sent_tokenize(question_text)
        for sentence in sentences:
            sentences_data.append({'sentence': sentence, 'label': row['questionID']})

df_sentences = pd.DataFrame(sentences_data)

df_sentences.to_csv('processed_counsel_chat_sentences.csv', index=False)
