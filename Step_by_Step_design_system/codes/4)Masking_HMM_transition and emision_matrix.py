# Define the file paths
input_file_path = 'A_faker-predistion.txt'     # This file name need to change with predicted file from rela world or Faker data 
output_file_path = 'AUG_replace10.txt'

# Function to process the file and replace the tokens
def replace_tokens(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        sentence_tokens = []
        sentence_labels = []
        sentence_number = 1  # To keep track of sentence numbering

        for line in infile:
            # Check for a sentence line
            if line.startswith("Sentence"):
                if sentence_tokens and sentence_labels:
                    # Process the previous sentence before moving to the next
                    process_and_write_sentence(outfile, sentence_number, sentence_tokens, sentence_labels)
                    sentence_number += 1  # Increment sentence number for the next sentence
                
                # Reset for the new sentence
                sentence_tokens = []
                sentence_labels = []
            # Check for Tokens line
            elif "Tokens:" in line:
                tokens_line = line.split("Tokens:")[1].strip()
                # Remove brackets and quotes
                sentence_tokens = eval(tokens_line)
            # Check for Labels line
            elif "Labels:" in line:
                labels_line = line.split("Labels:")[1].strip()
                sentence_labels = eval(labels_line)
        
        # Process the last sentence in the file if it exists
        if sentence_tokens and sentence_labels:
            process_and_write_sentence(outfile, sentence_number, sentence_tokens, sentence_labels)

# Function to process and write a single sentence
def process_and_write_sentence(outfile, sentence_number, tokens, labels):
    # Define synonyms
    synonyms_for_living = ['living','go', 'be', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'keep','animation']
    synonyms_for_owner = ['owner', 'possessor', 'proprietor']
    synonyms_for_email = ['email', 'mail', 'electronicmail']
    synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
    synonyms_for_security_code = ['securitycode', 'CVV', 'CVC', 'CVV2', 'cardverificationcode','socialecuritynumber']
    synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
    synonyms_for_IP_address = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
    synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
    synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
    synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
    synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']
    synonyms_for_bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']
    synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postcode']
    synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

    # Check if the first token's label is T1-Na
    if labels[0] == 'T1-Na' and len(tokens) > 1:
        tokens[0] = 'Name'
        tokens[1] = 'Last-Name'

    # Replace tokens based on specific criteria
    for i in range(len(tokens) - 1):
        # Replace '$' followed by any token
        if tokens[i] == '$':
            tokens[i + 1] = 'Money-amount'
        
        # Replace email tokens
        if tokens[i] in synonyms_for_email:
            tokens[i + 1] = 'EMAIL_value'
        
        # Replace owner tokens
        if tokens[i] in synonyms_for_owner:
            tokens[i + 1] = 'Name'
            if i + 2 < len(tokens):
                tokens[i + 2] = 'Last-Name'
        
        # Replace birthday-related tokens
        if tokens[i] in ['birthday', 'born', 'date birth']:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'Birthday_value'
        
        # Replace living-related tokens
        if tokens[i] in synonyms_for_living:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'Home-address'
        
        # Replace SSN-related tokens
        if tokens[i] in synonyms_for_ssn:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'SSN_values'

        # Replace IP address tokens
        if tokens[i] in synonyms_for_IP_address:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'IP_value'
        
        # Replace credit card-related tokens
        if tokens[i] in synonyms_for_credit_card:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'credit-value'
        
        # Replace security code-related tokens
        if tokens[i] in synonyms_for_security_code:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'seccode-value'

        # Replace charge-related tokens
        #if tokens[i] in synonyms_for_charge:
            #if i + 1 < len(tokens):
                #tokens[i + 1] = 'charge-value'

        # Replace phone number-related tokens
        if tokens[i] in synonyms_for_phone_number:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'phone_value'

        # Replace bank name-related tokens
        if tokens[i] in synonyms_for_bank_name:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'bank_value'

        # Replace website-related tokens
        if tokens[i] in synonyms_for_website:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'website_value'

        # Replace zip code-related tokens
        if tokens[i] in synonyms_for_zip_code:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'zipcode_value'

        # Replace country name-related tokens
        if tokens[i] in synonyms_for_country:
            if i + 1 < len(tokens):
                tokens[i + 1] = 'countryname_value'

    # Construct the sentence with updated tokens and labels
    updated_tokens_line = "Tokens: " + str(tokens)
    updated_labels_line = "Labels: " + str(labels)  # Keep labels unchanged
    outfile.write(f"Sentence {sentence_number}:\n{updated_tokens_line}\n{updated_labels_line}\n\n")

# Call the function to perform the replacement
replace_tokens(input_file_path, output_file_path)

print(f"Updated tokens saved to {output_file_path}")


######################################################################################
# Define the file paths
input_file_path = 'AUG_replace10.txt'
output_file_path = 'AUG_replace11.txt'

# Function to process the file and replace tokens
def replace_tokens(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        sentence_tokens = []
        sentence_labels = []
        sentence_number = 1  # To keep track of sentence numbering

        for line in infile:
            # Check for a sentence line
            if line.startswith("Sentence"):
                if sentence_tokens and sentence_labels:
                    # Process the previous sentence before moving to the next
                    process_and_write_sentence(outfile, sentence_number, sentence_tokens, sentence_labels)
                    sentence_number += 1  # Increment sentence number for the next sentence
                
                # Reset for the new sentence
                sentence_tokens = []
                sentence_labels = []
            # Check for Tokens line
            elif "Tokens:" in line:
                tokens_line = line.split("Tokens:")[1].strip()
                # Remove brackets and quotes
                sentence_tokens = eval(tokens_line)
            # Check for Labels line
            elif "Labels:" in line:
                labels_line = line.split("Labels:")[1].strip()
                sentence_labels = eval(labels_line)
        
        # Process the last sentence in the file if it exists
        if sentence_tokens and sentence_labels:
            process_and_write_sentence(outfile, sentence_number, sentence_tokens, sentence_labels)

# Function to process and write a single sentence
def process_and_write_sentence(outfile, sentence_number, tokens, labels):
    # Define synonym groups for replacement
    replacements = {
        'bank balance': ['bank balance', 'savings', 'funds', 'capital', 'wealth', 'balance', 'assets', 'money', 'income', 'equity', 'liabilities'],
        'charge': ['charge', 'fee', 'expense', 'cost', 'transaction'],
        'living': ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep'],
        'owner': ['possessor', 'owner', 'proprietor'],
        'IP address': ['IP', 'IP address', 'networkaddress', 'internetprotocol'],
        'SSN': ['SSN', 'socialsecuritynumber', 'IDnumber'],
        'credit card': ['creditcard', 'debitcard', 'paymentcard', 'card'],
        'email': ['email', 'mail', 'electronicmail'],
        'security code': ['securitycode', 'CVV', 'CVC', 'CVV2', 'cardverificationcode'],
        'birthday': ['born', 'birthday', 'datebirth'],
        'country': ['country', 'nation', 'state', 'land', 'territory'],
        'zip-code': ['zipcode', 'postalcode', 'zip', 'postcode'],
        'website': ['website', 'webpage', 'homepage', 'internetpage', 'webportal'],
        'bank_name': ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice'],
        'phone_number': ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone'],
        
    }

    # Replace tokens based on the replacement dictionary
    for i in range(len(tokens)):
        for key, synonyms in replacements.items():
            if tokens[i] in synonyms:
                tokens[i] = key
                break  # Exit loop once replacement is made to avoid duplicate checks

    # Construct the sentence with updated tokens and labels
    updated_tokens_line = "Tokens: " + str(tokens)
    updated_labels_line = "Labels: " + str(labels)  # Keep labels unchanged
    outfile.write(f"Sentence {sentence_number}:\n{updated_tokens_line}\n{updated_labels_line}\n\n")

# Call the function to perform the replacement
replace_tokens(input_file_path, output_file_path)

print(f"Updated tokens saved to {output_file_path}")

##################################################################################Transaction_Added(Labels and Tokens)
import re

# Defined labels
labels = ['T4-T1', 'T1-St', 'T1-Na', 'T1-La','T1-Bi','T1-Ss','T2-Mo','T4-T2','T1-Count',
'T1-Pho','T1-Zip','T3-web','T4-T3', 'T3-Ip','T2-credit','T2-Secode','T3-Em','T2-bank', 'O']
 
def read_data(file_path):
    sentences = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_tokens = []
        current_labels = []
        
        for line in lines:
            line = line.strip()
            if line.startswith("Tokens:"):
                # Extract tokens
                tokens = eval(line.split("Tokens:")[1].strip())
                current_tokens.extend(tokens)
            elif line.startswith("Labels:"):
                # Extract labels
                labels = eval(line.split("Labels:")[1].strip())
                current_labels.extend(labels)
                sentences.append((current_tokens, current_labels))
                current_tokens = []
                current_labels = []
    
    return sentences

def generate_transitions(sentences):
    output_lines = []
    
    for idx, (tokens, labels) in enumerate(sentences):
        output_lines.append(f"Sentence {idx + 1}::")
        output_lines.append(f"Tokens: {tokens}")
        output_lines.append(f"Labels: {labels}")
        
        # Generate transition pairs for labels
        label_transitions = [(labels[i], labels[i + 1]) for i in range(len(labels) - 1)]
        output_lines.append(f"Label Transitions: {label_transitions}")
        
        # Generate transition pairs for tokens
        token_transitions = [(tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1)]
        output_lines.append(f"Token Transitions: {token_transitions}")
        
        output_lines.append("")  # Blank line for sentence separation
    
    return output_lines

# Save to file
def save_to_file(filename, data):
    with open(filename, 'w') as f:
        for line in data:
            f.write(f"{line}\n")

# Main function
def main():
    input_file = 'AUG_replace11.txt'
    output_file = 'B_Transition11.txt'
    sentences = read_data(input_file)
    transition_data = generate_transitions(sentences)
    save_to_file(output_file, transition_data)

if __name__ == "__main__":
    main()


########################################################################################################
import re
import numpy as np

# Define the path to the input and output files
input_file = 'B_Transition11.txt'
output_file = 'B_T_matrix11.txt'

# Define the labels
labels = ['T4-T1', 'T1-St', 'T1-Na', 'T1-La','T1-Bi','T1-Ss','T2-Mo','T4-T2','T1-Count',
'T1-Pho','T1-Zip','T3-web','T4-T3', 'T3-Ip','T2-credit','T2-Secode','T3-Em','T2-bank', 'O']

# Create a mapping from labels to indices
label_index = {label: i for i, label in enumerate(labels)}

# Initialize a transition count matrix
transition_counts = np.zeros((len(labels), len(labels)))

# Read the input file and process each sentence
with open(input_file, 'r') as file:
    content = file.read()

# Split the content into sentences
sentences = content.split('Sentence')
for sentence in sentences[1:]:  # Skip the first split as it's empty
    # Extract labels using regex
    label_match = re.search(r'Labels: \[(.*?)\]', sentence)
    if label_match:
        label_list = label_match.group(1).replace("'", "").replace(" ", "").split(',')
        print("Extracted Labels:", label_list)  # Debugging

        # Calculate transitions
        for i in range(len(label_list) - 1):
            from_label = label_list[i]
            to_label = label_list[i + 1]
            print(f"Transition from {from_label} to {to_label}")  # Debugging
            if from_label in label_index and to_label in label_index:
                transition_counts[label_index[from_label], label_index[to_label]] += 1
            else:
                print(f"Label {from_label} or {to_label} not in label_index!")  # Debugging

# Calculate transition probabilities
transition_probabilities = np.zeros_like(transition_counts, dtype=float)
for i in range(len(labels)):
    row_sum = transition_counts[i].sum()
    if row_sum > 0:
        transition_probabilities[i] = transition_counts[i] / row_sum

# Create a formatted transition matrix for output
with open(output_file, 'w') as f:
    f.write("Transition Matrix:\n\n")
    f.write(" " * 12 + " ".join(f"{label:>8}" for label in labels) + "\n")
    f.write("-" * (12 + 9 * len(labels)) + "\n")  # Adjust line length based on the number of labels
    
    for i, from_label in enumerate(labels):
        f.write(f"{from_label:>10} | ")
        for j in range(len(labels)):
            f.write(f"{transition_probabilities[i, j]:>8.4f} ")
        f.write("\n")

print(f"Transition matrix saved to {output_file}.")

######################################################################################################################
import re
from collections import defaultdict

# Define the labels and observed states (tokens)
labels = [
    'T4-T1', 'T1-St', 'T1-Na', 'T1-La','T1-Bi','T1-Ss','T2-Mo','T4-T2','T1-Count',
'T1-Pho','T1-Zip','T3-web','T4-T3', 'T3-Ip','T2-credit','T2-Secode','T3-Em','T2-bank','O'
]
observed_states = [
    "$", ".", "Birthday_value", "EMAIL_value", "Home-address", 
    "IP address", "IP_value", "Last-Name", "Money-amount", 
    "Name", "SSN", "SSN_values", "bank balance", "birthday", 
     "charge", "credit card", "email","living", "owner","credit-value","seccode-value","securitycode","phone_value", 
     "bank_value","website_value", "zipcode_value","countryname_value","phone_number","bank_name","website", "zip-code","country"
]

# Initialize dictionaries for counting tokens and labels
token_count = defaultdict(lambda: defaultdict(int))
label_count = defaultdict(int)

# Read the data from the B_Transition.txt file
with open('B_Transition11.txt', 'r') as file:
    content = file.read()
    sentences = content.split('Sentence ')
    
    for sentence in sentences:
        if sentence.strip():
            # Extract the labels and tokens using regex
            label_match = re.search(r'Labels:\s*\[(.*?)\]', sentence)
            token_match = re.search(r'Tokens:\s*\[(.*?)\]', sentence)
            
            if label_match and token_match:
                # Split the extracted strings into lists
                labels_in_sentence = [label.strip().strip("'") for label in label_match.group(1).split(',')]
                tokens_in_sentence = [token.strip().strip("'") for token in token_match.group(1).split(',')]
                
                # Count occurrences of each label and token pairs
                for label, token in zip(labels_in_sentence, tokens_in_sentence):
                    if label in labels:  # Ensure we only count specified labels
                        token_count[label][token] += 1
                        label_count[label] += 1

# Calculate emission probabilities
emission_matrix = defaultdict(lambda: defaultdict(float))

for label in labels:
    for token in observed_states:
        if label_count[label] > 0:
            # Calculate the probability of each token given the label
            emission_matrix[label][token] = token_count[label][token] / label_count[label]

# Create a string representation of the emission matrix for better readability
matrix_output = "Emission Matrix:\n"

# Column width for alignment
column_width = 15

# Add a header row for observed states
header_row = "Label".ljust(column_width)  # Start with the Label
header_row += " | ".join([f"{state:<{column_width}}" for state in observed_states])  # Add observed states with additional spacing
matrix_output += header_row + "\n"
matrix_output += "-" * (len(header_row)) + "\n"  # Adjust for total width

# Create a list to hold labels and their corresponding probabilities
rows = []

for label in labels:
    row = [f"{label:<{column_width}}"]  # Left align label
    for token in observed_states:
        # Format the emission probabilities with additional spacing
        row.append(f"{emission_matrix[label][token]:<{column_width}.4f}")  # Using < to left-align with specified width
    # Join the row with vertical separators
    rows.append(" | ".join(row))

# Add each row to the matrix output
for row in rows:
    matrix_output += row + "\n"
    # Add a long horizontal separator after each row
    matrix_output += "-" * len(header_row) + "\n"  

# Save the emission matrix to a text file
with open('B_E_matrix11.txt', 'w') as output_file:
    output_file.write(matrix_output)

print("Emission matrix has been calculated and saved as 'B_E_matrix.txt'.")











