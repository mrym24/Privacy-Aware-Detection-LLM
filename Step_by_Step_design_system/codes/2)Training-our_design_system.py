import numpy as np
import matplotlib.pyplot as plt  
from keras.models import Sequential
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Bidirectional, Dropout, BatchNormalization
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping, Callback  
import json
from keras.regularizers import l2
from keras.optimizers import Adam
import nltk
import re
import random
from faker import Faker
from sklearn.metrics import f1_score, precision_score, recall_score
import re
from faker import Faker

nltk.download('punkt')

fake = Faker()

# Function to generate fake website using a platform
def generate_fake_website(platform):
    return f"{fake.first_name().lower()}.{platform.lower()}.com"

fake = Faker()

import re

def load_data(file_path):
    sentences = []
    labels = []
    sentence = []
    label = []
    
    # Regular expression patterns for various data types
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    street_address_pattern = r'\d+\s[\w\s]+(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Dr|Drive|Ln|Lane|Ct|Court|Ter|Terrace|Pl|Place|Cir|Circle)\s(?:East|West|North|South)?'
    credit_card_pattern = r'\b(?:credit\s*card)\b'
    bank_balance_pattern = r'\b(?:bank\s*balance)\b'
    date_birth_pattern = r'\b(?:date\s*birth)\b'
    birthday_pattern = r'\b(?:\w+\s\d{1,2}\s\d{4})\b'
    ip_address_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    phone_keywords = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone', 'phone']
    phone_number_pattern = r"""
        \b(?:\+?\d{1,3}[-.\s]?)?                 # Optional country code, e.g., +1
        (?:\(\d{3}\)|\d{3})?[-.\s]?             # Area code, e.g., (123) or 123
        \d{3}[-.\s]?\d{4}                       # Main phone number, e.g., 456-7890
        (?:x\d+|X\d+)?                          # Optional extension, e.g., x12345
    """
    synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']
    popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']
    synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

    # Regular expression to match popular platform patterns
    platform_pattern = r'\b(?:[a-zA-Z0-9._%+-]+)\.(?:' + '|'.join(popular_platforms) + r')\b'

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # New sentence start
            if line.startswith("Sentence"):
                if sentence:
                    sentences.append(sentence)
                    labels.append(label)
                sentence = []
                label = []
            # Tokens and Labels extraction
            elif line.startswith("Tokens:"):
                tokens = line.split(': ')[1].strip().strip('[]').replace("'", "").split(", ")
                
                skip_next = False
                group_tokens = []  # This list will hold grouped tokens
                
                for i, token in enumerate(tokens):
                    if skip_next:
                        skip_next = False
                        continue
                    
                    # Check if the token matches phone-related synonyms
                    if token.lower() in phone_keywords and i + 1 < len(tokens):
                        next_token = tokens[i + 1]
                        if re.match(phone_number_pattern, next_token, re.VERBOSE):
                            # Combine phone-related token and the number as one token
                            sentence.append(f'{token}_{next_token}')
                            skip_next = True  # Skip the next token since it's part of the phone number
                            continue
                    
                    # Check if the token matches a web-related synonym
                    if token.lower() in synonyms_for_website:
                        sentence.append(token)  # Add web synonym as a single token
                    
                    # Check if the token matches a platform pattern
                    elif re.match(platform_pattern, token):
                        sentence.append(token)  # Add platform pattern as a single token
                    
                    # Handle country synonyms
                    elif token.lower() in synonyms_for_country and i + 1 < len(tokens):
                        next_token = tokens[i + 1]
                        sentence.append(token)  # Add country synonym as one token
                        sentence.append(next_token)  # Assume the next token as one (e.g., "Sri Lanka")
                        skip_next = True  # Skip the next token since it's already included
                        continue
                    
                    # Check for other patterns
                    elif re.match(email_pattern, token):
                        sentence.append(token)  
                    elif re.match(street_address_pattern, token):
                        sentence.append(token) 
                    elif re.match(credit_card_pattern, token):
                        sentence.append(token)  
                    elif re.match(bank_balance_pattern, token):
                        sentence.append(token)  
                    elif re.match(date_birth_pattern, token):
                        sentence.append(token)  
                    elif re.match(birthday_pattern, token):
                        sentence.append(token)  
                    elif re.match(ip_address_pattern, token):
                        sentence.append(token) 
                    else:
                        sentence.append(token)  

            elif line.startswith("Labels:"):
                label_line = line.split(': ')[1].strip().strip('[]').replace("'", "").split(", ")
                label = label_line
        
        # Add last sentence for training
        if sentence:
            sentences.append(sentence)
            labels.append(label)

    return sentences, labels

def preprocess_data(sentences, labels, max_len=100):

    # Map words to integers using NLTK tokenization
    word_index = {word: i + 1 for i, word in enumerate(set(word for sentence in sentences for word in sentence))}
    
    # Tokenizing all sentences without filtering
    sequences = [[word_index[word] for word in sentence] for sentence in sentences]
    
    # Padding sequences to uniform length
    X = pad_sequences(sequences, maxlen=max_len, padding='post')
    
    # Convert labels to integers and pad them
    label_tokenizer = {label: i + 1 for i, label in enumerate(set(label for label_list in labels for label in label_list))}
    label_sequences = [[label_tokenizer[label] for label in label_list] for label_list in labels]
    y = pad_sequences(label_sequences, maxlen=max_len, padding='post')
    
    # (one-hot encoding)
    y = [to_categorical(i, num_classes=len(label_tokenizer) + 1) for i in y]
    
    return X, np.array(y), word_index, label_tokenizer

def create_model(input_dim, output_dim, input_length):
    model = Sequential()
    
    # Embedding layer
    model.add(Embedding(input_dim=input_dim, output_dim=64, input_length=input_length))
    
    # First LSTM layer
    model.add(Bidirectional(LSTM(units=120, return_sequences=True, recurrent_dropout=0.1)))
    model.add(Dropout(0.4))
    
    # Batch normalization
    model.add(BatchNormalization())


    model.add(TimeDistributed(Dense(64, activation='relu')))
    

    # Final output layer
    model.add(TimeDistributed(Dense(output_dim, activation='softmax', kernel_regularizer=l2(0.001))))  

   
    optimizer = Adam(learning_rate=learning_rate) 
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    return model

# Callback for calculating F1, precision, and recall after each epoch
class F1ScoreCallback(Callback):
    def __init__(self, validation_data):
        super().__init__()
        self.validation_data = validation_data
        self.f1_scores = []
        self.precision_scores = []
        self.recall_scores = []

    def on_epoch_end(self, epoch, logs=None):
        X_val, y_val = self.validation_data
        y_pred = self.model.predict(X_val)
        y_pred_classes = np.argmax(y_pred, axis=-1)
        y_true_classes = np.argmax(y_val, axis=-1)

        y_pred_flat = y_pred_classes.flatten()
        y_true_flat = y_true_classes.flatten()

        f1 = f1_score(y_true_flat, y_pred_flat, average='weighted')
        precision = precision_score(y_true_flat, y_pred_flat, average='weighted')
        recall = recall_score(y_true_flat, y_pred_flat, average='weighted')

        self.f1_scores.append(f1)
        self.precision_scores.append(precision)
        self.recall_scores.append(recall)

        print(f'\nEpoch {epoch + 1}: F1 Score: {f1:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}')

# Load and preprocess data without filtering 'O' labels
sentences, labels = load_data('A_Format_AUG4.txt')  # Replace with your actual file path

# Preprocess the loaded data
X, y, word_index, label_word_index = preprocess_data(sentences, labels)

# Save tokenizer info (word index) to a file
with open('tokenizer_info_70.json', 'w') as f:
    json.dump(word_index, f)

# Save tokenized data
np.save('X_tokenized70.txt', X)
np.save('y_tokenized70.txt', y)

# Save label and word mappings
with open('word_index70.json', 'w') as f:
    json.dump(word_index, f)

with open('label_word_index70.json', 'w') as f:
    json.dump(label_word_index, f)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

learning_rate = 0.0001  

# Create the model
model = create_model(input_dim=len(word_index) + 1, output_dim=len(label_word_index) + 1, input_length=X_train.shape[1])

# Define early stopping 
early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)

# Add the F1 score callback
f1_score_callback = F1ScoreCallback(validation_data=(X_test, np.array(y_test)))

# early stopping
history = model.fit(X_train, np.array(y_train), batch_size=32, epochs=1000, 
                    validation_data=(X_test, np.array(y_test)), 
                    callbacks=[early_stopping, f1_score_callback])

# Save the model
model.save('ner_model_n1_70.h5')

# Save F1, Precision, and Recall results to a file
with open('f1_precision_recall_results.txt', 'w') as f:
    f.write("F1 Scores per Epoch:\n")
    f.write(str(f1_score_callback.f1_scores) + "\n")
    f.write("Precision Scores per Epoch:\n")
    f.write(str(f1_score_callback.precision_scores) + "\n")
    f.write("Recall Scores per Epoch:\n")
    f.write(str(f1_score_callback.recall_scores) + "\n")

# Plot training & validation accuracy values
plt.subplot(1, 3, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(loc='upper left')

# Plot training & validation loss values
plt.subplot(1, 3, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(loc='upper left')

# Plot F1 Score, Precision, and Recall
plt.subplot(1, 3, 3)
plt.plot(f1_score_callback.f1_scores, label='F1 Score')
plt.plot(f1_score_callback.precision_scores, label='Precision')
plt.plot(f1_score_callback.recall_scores, label='Recall')
plt.title('Metrics over Epochs')
plt.ylabel('Score')
plt.xlabel('Epoch')
plt.legend(loc='upper left')


plt.tight_layout()


plt.show()


# Evaluate the model accuracy on the test set
test_loss, test_accuracy = model.evaluate(X_test, np.array(y_test))
print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}')

print("Training complete and results saved!")

# Evaluate the model accuracy on the training set
train_loss, train_accuracy = model.evaluate(X_train, np.array(y_train))
print(f'Training Loss: {train_loss:.4f}, Training Accuracy: {train_accuracy:.4f}')

print("Training complete and results saved!")
