import numpy as np
import json
from transformers import BertTokenizer, TFBertModel
from keras.models import load_model
from keras.utils import custom_object_scope

# Load the trained model with custom scope for TFBertModel
with custom_object_scope({'TFBertModel': TFBertModel}):
    model = load_model("trained_model_bert8.h5")

# Load the tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Load label map (the label-to-integer mapping used during training)
with open('label_map8.json', 'r') as f:
    label_map = json.load(f)

# Example input sentence
input_text = """Sentence 1:
Tokens: ['phonenumber', '001-857-579-4376x108', 'webportal', 'rachelwatson.twitter.com', 'proprietor', 'Kiara', 'Mullins', 'email', 'vazquezjohn@taylor-hernandez.com', '.']"""

# Preprocess input text to match tokenization during training
def preprocess_input(input_text, tokenizer, max_length=120):
    # Extract the sentence from the input string (no need to split tokens manually)
    sentence = input_text.split("Tokens: ")[1].strip().strip('[]').replace("'", "").replace(", ", " ")

    # Tokenize the sentence using BERT tokenizer
    tokenized_data = tokenizer(
        sentence,
        padding='max_length',
        truncation=True,
        max_length=max_length,
        return_tensors='tf'
    )
    return tokenized_data

# Preprocess the input sentence
tokenized_data = preprocess_input(input_text, tokenizer)

# Extract inputs for the model (input_ids, attention_mask, token_type_ids)
input_ids = tokenized_data['input_ids']
attention_mask = tokenized_data['attention_mask']
token_type_ids = tokenized_data['token_type_ids']

# Create a dictionary with the inputs for the model
inputs = {
    'input_ids': input_ids,
    'attention_mask': attention_mask,
    'token_type_ids': token_type_ids
}

# Predict using the trained model
predictions = model.predict(inputs)

# Convert predictions to label IDs (get the label index with the highest probability)
predicted_labels = np.argmax(predictions, axis=-1)

# Reverse the label map (from integer to label)
reverse_label_map = {v: k for k, v in label_map.items()}

# Map the predicted label indices to their corresponding labels
predicted_labels = [reverse_label_map[label_id] for label_id in predicted_labels[0]]

# Convert input_ids to tokens
tokens = tokenizer.convert_ids_to_tokens(input_ids[0].numpy())

# Filter out special tokens ([CLS], [SEP], [PAD]) from the final output
filtered_tokens = []
filtered_labels = []

for token, label in zip(tokens, predicted_labels):
    if token not in ['[CLS]', '[SEP]', '[PAD]']:
        filtered_tokens.append(token)
        filtered_labels.append(label)

# Print the filtered tokens and their predicted labels
for token, label in zip(filtered_tokens, filtered_labels):
    print(f"Token: {token}, Predicted Label: {label}")
