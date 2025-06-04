import numpy as np
import re
import json
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

# Load the trained model
model = load_model('ner_model_n1_70.h5')

# Load word index and label index
with open('word_index70.json', 'r') as f:
    word_index = json.load(f)

with open('label_word_index70.json', 'r') as f:
    label_word_index = json.load(f)

reverse_label_word_index = {v: k for k, v in label_word_index.items()}

# Preprocessing function to handle sentences without labels
def preprocess_input(tokens, max_len=100):
    sequence = [word_index.get(token, 0) for token in tokens]
    padded_sequence = pad_sequences([sequence], maxlen=max_len, padding='post')
    return padded_sequence

# Predict function

def predict_labels(model, tokens, max_len=100):
    X_input = preprocess_input(tokens, max_len)
    y_pred = model.predict(X_input)
    y_pred_classes = np.argmax(y_pred, axis=-1)
    predicted_labels = [reverse_label_word_index.get(label_id, 'O') for label_id in y_pred_classes[0]]
    return predicted_labels[:len(tokens)]

# Read and parse example file for prediction
def parse_example_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    sentences = re.findall(r"Sentence \d+:\nTokens: \[(.*?)\]", content)
    token_lists = [s.replace("'", "").split(', ') for s in sentences]
    return token_lists

# Read and parse ground truth labels
def parse_ground_truth(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    label_sentences = re.findall(r"Labels: \[(.*?)\]", content)
    label_lists = [l.replace("'", "").split(', ') for l in label_sentences]
    return label_lists

# Calculate accuracy
def calculate_accuracy(predicted_labels, actual_labels):
    correct = sum(p == a for p, a in zip(predicted_labels, actual_labels))
    total = len(actual_labels)
    return correct / total if total > 0 else 0

# Main function to process files and predict labels
def main():
    example_file = 'A_Format-faker-data.txt'
    ground_truth_file = 'A_Format_AUG.txt'
    
    # Parse input files
    token_lists = parse_example_file(example_file)
    actual_labels = parse_ground_truth(ground_truth_file)
    
    predictions = []
    overall_correct = 0
    overall_total = 0
    
    with open('A_faker-predistion.txt', 'w') as f:
        for i, tokens in enumerate(token_lists):
            predicted_labels = predict_labels(model, tokens)
            predictions.append(predicted_labels)
            
            f.write(f"Sentence {i+1}:\n")
            f.write(f"Tokens: {tokens}\n")
            f.write(f"Predicted Labels: {predicted_labels}\n")
            
            if i < len(actual_labels):  # Calculate accuracy if ground truth is available
                accuracy = calculate_accuracy(predicted_labels, actual_labels[i])
                overall_correct += sum(p == a for p, a in zip(predicted_labels, actual_labels[i]))
                overall_total += len(actual_labels[i])
                f.write(f"Actual Labels: {actual_labels[i]}\n")
                f.write(f"Sentence Accuracy: {accuracy:.4f}\n\n")
            else:
                f.write("Actual Labels: Not Available\n\n")
        
        if overall_total > 0:
            overall_accuracy = overall_correct / overall_total
            f.write(f"Overall Accuracy: {overall_accuracy:.4f}\n")

if __name__ == "__main__":
    main()