import numpy as np
import time
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score
from keras.models import Model
from keras.layers import Input, LSTM, Bidirectional, Dense
from keras.callbacks import EarlyStopping, Callback
from transformers import BertTokenizer, TFBertModel
from keras.optimizers import Adam
from keras import layers
import re
from keras.optimizers import RMSprop


# Regular expression patterns for various data types
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zAZ0-9.-]+\.[a-zAZ0-9]{2,}'
street_address_pattern = r'\d+\s[\w\s]+(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Dr|Drive|Ln|Lane|Ct|Court|Ter|Terrace|Pl|Place|Cir|Circle)\s(?:East|West|North|South)?'
credit_card_pattern = r'\b(?:credit\s*card)\b'
bank_balance_pattern = r'\b(?:bank\s*balance)\b'
date_birth_pattern = r'\b(?:date\s*birth)\b'
birthday_pattern = r'\b(?:\w+\s\d{1,2}\s\d{4})\b'
ip_address_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
phone_keywords = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone', 'phone']
phone_number_pattern = r"""
    \b(?:\+?\d{1,3}[-.\s]?)?                 # Optional country code
    (?:\(\d{3}\)|\d{3})?[-.\s]?             # Area code
    \d{3}[-.\s]?\d{4}                       # Main number
    (?:x\d+|X\d+)?                          # Extension
"""
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']
platform_pattern = r'\b(?:[a-zA-Z0-9._%+-]+)\.(?:' + '|'.join(popular_platforms) + r')\b'

# Function to load data and process tokens and labels
def load_data(file_path):
    sentences = []
    labels = []
    sentence = []
    label = []
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Sentence"):
                if sentence:
                    sentences.append(sentence)
                    labels.append(label)
                sentence = []
                label = []
            elif line.startswith("Tokens:"):
                tokens = line.split(': ')[1].strip('[]').replace("'", "").split(", ")
                skip_next = False
                for i, token in enumerate(tokens):
                    if skip_next:
                        skip_next = False
                        continue
                    if token.lower() in phone_keywords and i + 1 < len(tokens):
                        next_token = tokens[i + 1]
                        if re.match(phone_number_pattern, next_token, re.VERBOSE):
                            sentence.append(f'{token}_{next_token}')
                            skip_next = True
                            continue
                    elif token.lower() in synonyms_for_website:
                        sentence.append(token)
                    elif re.match(platform_pattern, token):
                        sentence.append(token)
                    elif token.lower() in synonyms_for_country and i + 1 < len(tokens):
                        next_token = tokens[i + 1]
                        sentence.append(token)
                        sentence.append(next_token)
                        skip_next = True
                        continue
                    elif re.match(email_pattern, token) or re.match(street_address_pattern, token) or \
                         re.match(credit_card_pattern, token) or re.match(bank_balance_pattern, token) or \
                         re.match(date_birth_pattern, token) or re.match(birthday_pattern, token) or re.match(ip_address_pattern, token):
                        sentence.append(token)
                    else:
                        sentence.append(token)

            elif line.startswith("Labels:"):
                label_line = line.split(': ')[1].strip('[]').replace("'", "").split(", ")
                label = label_line
        if sentence:
            sentences.append(sentence)
            labels.append(label)
    return sentences, labels

# Map labels to integers
def map_labels(labels):
    unique_labels = sorted(set(label for label_list in labels for label in label_list))
    label_map = {label: idx for idx, label in enumerate(unique_labels)}
    return label_map

# Tokenize and encode labels with subword handling
def tokenize_and_encode(sentences, labels, tokenizer, label_map, max_length):
    input_ids, attention_masks, encoded_labels, token_type_ids = [], [], [], []
    
    for sentence, label_list in zip(sentences, labels):
        tokens, label_ids = [], []
        
        for word, label in zip(sentence, label_list):
            word_tokens = tokenizer.tokenize(word)  # Tokenize the word
            
            # For the first token of the word, assign the correct label
            tokens.extend(word_tokens)
            label_ids.extend([label_map[label]] + [label_map[label]] * (len(word_tokens) - 1))
        
        # Tokenize the sentence (handling padding and truncation)
        tokenized_data = tokenizer(tokens, is_split_into_words=True, padding='max_length', truncation=True, max_length=max_length)
        
        input_ids.append(tokenized_data['input_ids'])
        attention_masks.append(tokenized_data['attention_mask'])
        encoded_labels.append(label_ids[:max_length] + [label_map['O']] * (max_length - len(label_ids)))
        
        # Set token_type_ids to all zeros (as we're working with single sentences)
        token_type_ids.append([0] * max_length)

    return np.array(input_ids), np.array(attention_masks), np.array(encoded_labels), np.array(token_type_ids)

# Define custom F1 score callback
class F1ScoreCallback(Callback):
    def __init__(self, val_data):
        self.val_data = val_data
        self.f1_scores = []
        self.precision_scores = []
        self.recall_scores = []

    def on_epoch_end(self, epoch, logs=None):
        # Access the validation data (ensure correct unpacking)
        val_input_ids, val_attention_mask, val_token_type_ids = self.val_data[0]

        # Get true labels
        val_true = self.val_data[1]

        # Make predictions
        val_pred = self.model.predict([val_input_ids, val_attention_mask, val_token_type_ids])
        val_pred_labels = np.argmax(val_pred, axis=-1)

        # Calculate metrics
        precision = precision_score(val_true.flatten(), val_pred_labels.flatten(), average='micro')
        recall = recall_score(val_true.flatten(), val_pred_labels.flatten(), average='micro')
        f1 = f1_score(val_true.flatten(), val_pred_labels.flatten(), average='micro')

        # Store scores
        self.precision_scores.append(precision)
        self.recall_scores.append(recall)
        self.f1_scores.append(f1)

        print(f"Epoch {epoch + 1} F1 Score: {f1:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}")

# Load data
file_path = "A_Format_AUG4.txt"
sentences, labels = load_data(file_path)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
label_map = map_labels(labels)
max_length = 120

input_ids, attention_masks, encoded_labels, token_type_ids = tokenize_and_encode(sentences, labels, tokenizer, label_map, max_length)
X_train, X_val, y_train, y_val = train_test_split(input_ids, encoded_labels, test_size=0.2, random_state=42)
X_train_attention, X_val_attention = train_test_split(attention_masks, test_size=0.2, random_state=42)
X_train_token_type, X_val_token_type = train_test_split(token_type_ids, test_size=0.2, random_state=42)

# Save tokenizer information (vocabulary)
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
with open('tokenizer_info_8120.json', 'w') as f:
    json.dump(bert_tokenizer.get_vocab(), f)

# Save tokenized training data
np.save('X_tokenized8120.npy', X_train)
np.save('y_tokenized8120.npy', y_train)

# Save word index (vocabulary)
with open('word_index8120.json', 'w') as f:
    json.dump(bert_tokenizer.get_vocab(), f)

# Save label-to-integer mapping
with open('label_word_index8120.json', 'w') as f:
    json.dump(label_map, f)

# Build the model
input_ids_layer = Input(shape=(max_length,), dtype='int32', name="input_ids")
attention_mask_layer = Input(shape=(max_length,), dtype='int32', name="attention_mask")
token_type_ids_layer = Input(shape=(max_length,), dtype='int32', name="token_type_ids")

bert_model = TFBertModel.from_pretrained("bert-base-uncased")
bert_output = bert_model(input_ids_layer, attention_mask=attention_mask_layer, token_type_ids=token_type_ids_layer)[0]

lstm_output = Bidirectional(LSTM(256, dropout=0.4, return_sequences=True))(bert_output)
attention_output = layers.Attention()([lstm_output, lstm_output])
output_layer = Dense(len(label_map), activation="softmax")(attention_output)

model = Model(inputs=[input_ids_layer, attention_mask_layer, token_type_ids_layer], outputs=output_layer)

# Compile the model
model.compile(optimizer=RMSprop(learning_rate=0.0001), loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Train the model with the custom callback
f1_callback = F1ScoreCallback(val_data=[(X_val, X_val_attention, X_val_token_type), y_val])
early_stopping_callback = EarlyStopping(patience=20, restore_best_weights=True)

start_time = time.time()

history = model.fit(
    [X_train, X_train_attention, X_train_token_type], 
    y_train, 
    validation_data=([X_val, X_val_attention, X_val_token_type], y_val),
    epochs=100, 
    batch_size=64, 
    callbacks=[f1_callback, early_stopping_callback]
)

end_time = time.time()
print(f"Training time: {end_time - start_time:.2f} seconds")

final_train_loss = history.history['loss'][-1]
final_val_loss = history.history['val_loss'][-1]
final_train_acc = history.history['accuracy'][-1]
final_val_acc = history.history['val_accuracy'][-1]

print(f"Final Training Loss: {final_train_loss:.4f}")
print(f"Final Validation Loss: {final_val_loss:.4f}")
print(f"Final Training Accuracy: {final_train_acc:.4f}")
print(f"Final Validation Accuracy: {final_val_acc:.4f}")



# Save the trained model

model.save("bert_lstm_ner_model8")
model.save("trained_model_bert8.h5")

# Save the label map for later use
with open('label_map8.json', 'w') as f:
    json.dump(label_map, f)

# Plot training and validation loss
plt.figure(figsize=(12, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid()
plt.show()

# Plot training and validation accuracy
plt.figure(figsize=(12, 6))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid()
plt.show()

# Plot F1 score over epochs (from callback)
plt.figure(figsize=(12, 6))
plt.plot(f1_callback.f1_scores, label='Validation F1 Score')
plt.title('Validation F1 Score Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('F1 Score')
plt.legend()
plt.grid()
plt.show()

# Plot Precision over epochs
plt.figure(figsize=(12, 6))
plt.plot(f1_callback.precision_scores, label='Validation Precision')
plt.title('Validation Precision')
plt.xlabel('Epochs')
plt.ylabel('Precision')
plt.legend()
plt.grid()
plt.show()

# Plot Recall over epochs
plt.figure(figsize=(12, 6))
plt.plot(f1_callback.recall_scores, label='Validation Recall')
plt.title('Validation Recall')
plt.xlabel('Epochs')
plt.ylabel('Recall')
plt.legend()
plt.grid()
plt.show()
