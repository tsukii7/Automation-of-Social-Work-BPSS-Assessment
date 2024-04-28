import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from torch.utils.data import DataLoader

# Load dataset
data_path = '../data/csv/sentences_with_labels.csv'
df = pd.read_csv(data_path, encoding='GBK')
print(df.head())

# Label to id
label_to_id = {'N': 0, 'B': 1, 'P': 2, 'S': 3}
id_to_label = {v: k for k, v in label_to_id.items()}  # 反向映射

# Load tokenizer and model
model_path = '../exp2/model/bert_coarse_grained_classification'
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path, num_labels=len(label_to_id))

# Prepare dataset
class TextDataset(torch.utils.data.Dataset):
    def __init__(self, texts, tokenizer, max_len=512):
        self.encodings = tokenizer(texts, truncation=True, padding='max_length', max_length=max_len)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        return item

    def __len__(self):
        return len(self.encodings.input_ids)

# Tokenize texts
dataset = TextDataset(df['sentence'].tolist(), tokenizer)

# DataLoader for managing batches
loader = DataLoader(dataset, batch_size=16, shuffle=False)

# Prediction function
def predict(model, dataloader):
    model.eval()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    predictions = []
    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=-1)
            predictions.extend(preds.cpu().numpy())
    return predictions

# Run prediction
predicted_label_ids = predict(model, loader)
df['BERT_label'] = [id_to_label[id] for id in predicted_label_ids]

# Save results
output_path = '../data/csv/predicted_sentences_with_labels.csv'
df.to_csv(output_path, index=False)
print(f"Predictions saved to {output_path}")
