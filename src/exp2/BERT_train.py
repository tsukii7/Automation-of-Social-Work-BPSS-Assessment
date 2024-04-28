import pandas as pd
from datasets import load_metric
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset

data_path = '../data/csv/chat_sentences_labeled_fine_grained.csv'
df = pd.read_csv(data_path, encoding='GBK')

print(df.head())

label_to_id = {'N': 0, 'B': 1, 'P': 2, 'S': 3}

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
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(set(label_to_id.values())))
print("Model and tokenizer have been loaded.")

# split dataset
train_texts, temp_texts, train_labels, temp_labels = train_test_split(df['sentence'].tolist(), df['label'].tolist(), test_size=0.2, random_state=42)
val_texts, test_texts, val_labels, test_labels = train_test_split(temp_texts, temp_labels, test_size=0.2, random_state=42)

# prepare datasets
train_dataset = CustomDataset(train_texts, train_labels, tokenizer)
val_dataset = CustomDataset(val_texts, val_labels, tokenizer)
test_dataset = CustomDataset(test_texts, test_labels, tokenizer)

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

# train and evaluate
trainer.train()
eval_results = trainer.evaluate()
print(eval_results)

# predict test set
test_results = trainer.predict(test_dataset)
predicted_label_ids = test_results.predictions.argmax(axis=-1)

# calculate metrics
test_accuracy = accuracy_metric.compute(predictions=predicted_label_ids, references=test_results.label_ids)['accuracy']
test_recall = recall_metric.compute(predictions=predicted_label_ids, references=test_results.label_ids, average='macro')['recall']
test_f1 = f1_metric.compute(predictions=predicted_label_ids, references=test_results.label_ids, average='macro')['f1']

print(f"Test Accuracy: {test_accuracy}")
print(f"Test Recall: {test_recall}")
print(f"Test F1 Score: {test_f1}")

model_path = 'model/bert_coarse_grained_classification'

model.save_pretrained(model_path)

tokenizer.save_pretrained(model_path)

print(f"Model and tokenizer have been saved to {model_path}")
