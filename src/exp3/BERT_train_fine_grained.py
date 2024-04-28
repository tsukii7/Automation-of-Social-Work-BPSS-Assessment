import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score
from torch.utils.data import Dataset
import torch

# Define a custom dataset class
class CustomDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.tokenizer = tokenizer
        self.texts = texts
        # Convert labels to a tensor of type Long
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        tokenized_input = self.tokenizer(self.texts[idx], padding='max_length', truncation=True, max_length=512)
        return {
            "input_ids": torch.tensor(tokenized_input['input_ids']),
            "attention_mask": torch.tensor(tokenized_input['attention_mask']),
            "labels": self.labels[idx]
        }

# Load data
data_path = '../data/csv/chat_sentences_labeled_fine_grained.csv'
df = pd.read_csv(data_path, encoding='GBK')
df = df[df['label'] == 'B']

# Check if there's any NaN and remove or impute them
assert not df['sublabel'].isnull().any(), "NaN values found in 'sublabel' column."

# Convert 'sublabel' to integer and subtract 1 if labels start at 1
df['sublabel'] = df['sublabel'].astype(int) - 1

# Assert that labels are in the range [0, num_classes - 1]
num_labels = df['sublabel'].nunique()
assert df['sublabel'].between(0, num_labels - 1).all(), "Labels are outside the range [0, num_classes - 1]."


texts = df['sentence'].tolist()
labels = df['sublabel'].tolist()  # Using 'sublabel' as the target

# Prepare the tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Create dataset
dataset = CustomDataset(texts, labels, tokenizer)

# Split data
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

# Load model with the number of labels equal to the unique values in 'sublabel'
num_labels = df['sublabel'].nunique()
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_labels)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
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

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=lambda p: {'accuracy': accuracy_score(p.label_ids, p.predictions.argmax(-1)),
                               'recall': recall_score(p.label_ids, p.predictions.argmax(-1), average='weighted'),
                               'f1': f1_score(p.label_ids, p.predictions.argmax(-1), average='weighted')}
)

# Train and evaluate
trainer.train()
eval_results = trainer.evaluate()

# Print evaluation results
print(eval_results)

print(f"Accuracy: {eval_results['eval_accuracy']}")
print(f"Recall: {eval_results['eval_recall']}")
print(f"F1 Score: {eval_results['eval_f1']}")

# Save the model and tokenizer
model_path = './bert_fine_grained_classification_biology_model'
# model_path = './bert_fine_grained_classification_psychology_model'
# model_path = './bert_fine_grained_classification_social_model'

model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)
