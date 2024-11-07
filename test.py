#!python /content/ClauseClassifier/main.py
#!pip install -r requirements.txt
import os 
os.environ["WANDB_DISABLED"]="true"
import pandas as pd
data = pd.read_csv("/content/ClauseClassifier/artifacts/data_ingestion/master_clauses.csv")
documents = []
labels = []
for index, row in data.iterrows():
    # Assuming the clause types are in columns following the document name
    for clause_type in data.columns[1:]:
        if not pd.isna(row[clause_type]):
            clauses = row[clause_type].split(';')  # Assuming clauses are separated by semicolons
            for clause in clauses:
                documents.append(clause)
                labels.append(clause_type)
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset, DatasetDict
# Tokenize the data
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
encodings = tokenizer(documents, truncation=True, padding=True)
# Convert labels to numeric format
label_dict = {label: idx for idx, label in enumerate(data.columns[1:])}
numeric_labels = [label_dict[label] for label in labels]
# Create dataset
dataset = Dataset.from_dict({
    'input_ids': encodings['input_ids'],
    'attention_mask': encodings['attention_mask'],
    'labels': numeric_labels
})
# Split into train and validation sets using the datasets library
dataset = dataset.train_test_split(test_size=0.1)
train_dataset = dataset['train']
val_dataset = dataset['test']

# Load the model
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(data.columns[1:]))

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Train the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)
## incase training on azure 
from transformers.integrations import MLflowCallbacks 
trainer.remove_classback(MLflowCallbacks)

trainer.train()