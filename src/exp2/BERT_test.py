import pandas as pd
from datasets import load_metric
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset

data_path = '../data/csv/chat_sentences_labeled_fine_grained.csv'
df = pd.read_csv(data_path, encoding='GBK')

print(df.head())

# label to id
label_to_id = {'N': 0, 'B': 1, 'P': 2, 'S': 3}
id_to_label = {v: k for k, v in label_to_id.items()}  # 反向映射

class CustomDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.tokenizer = tokenizer
        self.texts = texts
        self.labels = [label_to_id[label] for label in labels]

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        tokenized_input = self.tokenizer(self.texts[idx], padding='max_length', truncation=True, max_length=512)
        return {
            "input_ids": torch.tensor(tokenized_input['input_ids']),
            "attention_mask": torch.tensor(tokenized_input['attention_mask']),
            "labels": torch.tensor(self.labels[idx])
        }

# load model and tokenizer
model_path = 'model/bert_coarse_grained_classification'
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

train_texts, temp_texts, train_labels, temp_labels, train_index, temp_index = train_test_split(df['sentence'], df['label'], df.index, test_size=0.2, random_state=42, stratify=df['label'])
val_texts, test_texts, val_labels, test_labels, val_index, test_index = train_test_split(temp_texts, temp_labels, temp_index, test_size=0.5, random_state=42, stratify=temp_labels)

test_df = df.loc[test_index]

# prepare datasets
train_dataset = CustomDataset(train_texts.tolist(), train_labels.tolist(), tokenizer)
val_dataset = CustomDataset(val_texts.tolist(), val_labels.tolist(), tokenizer)
test_dataset = CustomDataset(test_texts.tolist(), test_labels.tolist(), tokenizer)

# load evaluation metrics
accuracy_metric = load_metric("accuracy")
recall_metric = load_metric("recall")
f1_metric = load_metric("f1")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = logits.argmax(axis=-1)
    accuracy = accuracy_metric.compute(predictions=predictions, references=labels)
    recall = recall_metric.compute(predictions=predictions, references=labels, average='macro')
    f1 = f1_metric.compute(predictions=predictions, references=labels, average='macro')
    return {
        "accuracy": accuracy['accuracy'],
        "recall": recall['recall'],
        "f1": f1['f1']
    }

# Training Arguments
training_args = TrainingArguments(
    output_dir='../results',
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=5,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model='f1'
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

# predict
test_results = trainer.predict(test_dataset)
predicted_label_ids = test_results.predictions.argmax(axis=-1)
predicted_labels = [id_to_label[id] for id in predicted_label_ids]

# calculate metrics
test_accuracy = accuracy_metric.compute(predictions=predicted_label_ids, references=test_results.label_ids)['accuracy']
test_recall = recall_metric.compute(predictions=predicted_label_ids, references=test_results.label_ids, average='macro')['recall']
test_f1 = f1_metric.compute(predictions=predicted_label_ids, references=test_results.label_ids, average='macro')['f1']

print(f"Test Accuracy: {test_accuracy}")
print(f"Test Recall: {test_recall}")
print(f"Test F1: {test_f1}")

test_df['BERT_label'] = predicted_labels

test_df['BERT_accuracy'] = (test_df['BERT_label'] == test_df['label']).astype(int)

# test_df.to_csv('./data/test_dataset_with_bert_labels.csv', index=False)
# print("Test dataset with BERT labels has been saved to './data/test_dataset_with_bert_labels.csv'.")

