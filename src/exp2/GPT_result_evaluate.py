import pandas as pd

csv_file_path = '../data/csv/test_dataset.csv'

data = pd.read_csv(csv_file_path, encoding='GBK')
print(data.head())

from sklearn.metrics import accuracy_score, recall_score, f1_score


true_labels = data['label']
gpt_labels = data['ChatGPT4_label']

true_labels = true_labels.astype(str)
gpt_labels = gpt_labels.astype(str)

accuracy = accuracy_score(true_labels, gpt_labels)
recall = recall_score(true_labels, gpt_labels, average='macro')
f1 = f1_score(true_labels, gpt_labels, average='macro')

print(f"Accuracy: {accuracy}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")
