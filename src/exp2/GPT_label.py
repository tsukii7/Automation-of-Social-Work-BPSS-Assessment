import os
import pandas as pd
import json
from openai import OpenAI
from util import prompt

SAVE_PERIOD = 25
csv_file_path = '../data/csv/chat_sentences.csv'
df = pd.read_csv(csv_file_path)

os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI()

system_message = {
    "role": "system",
    "content": prompt
}

ChatGPT4_labels = []

def create_chat_completion(paragraph):
    user_message = "Analyze the following text, each line for one sentence, labels within ['B', 'P', 'S', 'N']: \n" + paragraph
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            system_message,
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    return completion.choices[0].message.content

def extract_label_from_response(response):
    message_content = json.loads(response)
    labels = [sentence["Label"] for sentence in message_content["Sentences"]]
    return labels

def parse_csv_to_text():
    grouped_data = df.groupby('questionID')['sentence'].agg('\n'.join).reset_index()
    formatted_data = grouped_data.apply(lambda row: {'questionID': row['questionID'], 'text': row['sentence'],
                                                     'length': len(row['sentence'].split("\n"))}, axis=1).tolist()
    print(len(formatted_data))
    for i in range(len(formatted_data)):
        text = create_chat_completion(formatted_data[i].get('text'))
        print(formatted_data[i])
        labels = extract_label_from_response(text)
        print(labels)
        if "Social" in labels or "Psychological" in labels or "Biological" in labels:
            break
        for i in range(formatted_data[i].get('length')):
            if len(labels) <= i:
                ChatGPT4_labels.append("N")
            else:
                ChatGPT4_labels.append(labels[i])
        if i % SAVE_PERIOD == 0:
            update_csv_with_labels()


def update_csv_with_labels():
    if len(df) != len(ChatGPT4_labels):
        print("The number of labels does not match the number of sentences in the csv file.")
    df['ChatGPT4_label'] = pd.Series(ChatGPT4_labels)
    print("length of ChatGPT4_labels: ", len(ChatGPT4_labels))
    print("ChatGPT4_labels: ", ChatGPT4_labels)
    df.to_csv(csv_file_path, index=False)


parse_csv_to_text()
update_csv_with_labels()
print(ChatGPT4_labels)
