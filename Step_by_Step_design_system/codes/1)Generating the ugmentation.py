from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    # Randomly replace "living" with one of the given terms
    living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
    augmented_tokens = [random.choice(living_terms)]  # Start with a random term

    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }
    
    i = 1  # Start from the second token since "living" is already added
    while i < len(tokens):
        token = tokens[i]
        
        # Replace street address tokens after "Living"
        if token.isdigit() and tokens[i-1] == "living":
            building_number = fake.building_number()
            street_name = fake.word().capitalize()  # Single word for street name
            city = fake.city().split()[0]  # Single word for city
            street_address = f"{building_number} {street_name} St {city}"
            augmented_tokens.append(street_address)
            i += 4  # Skip the next 4 tokens that make up the full address in the original tokens
            
            synonyms_for_owner = ['possessor', 'owner', 'proprietor']  # Synonyms list
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Add a random synonym for "owner"
            augmented_tokens.append(get_unique_first_name())  # Unique first name
            augmented_tokens.append(get_unique_last_name())   # Unique last name
            i += 2  # Skip the name and surname tokens in the original tokens
            
        elif token == "birthday":
            augmented_tokens.append("birthday")
            month = random.choice(list(month_days.keys()))
            day = str(random.randint(1, month_days[month]))
            year = str(random.randint(1980, 2020))
            birthday = f"{month} {day} {year}"
            augmented_tokens.append(birthday)
            i += 3  # Skip the next 3 tokens that make up the date in the original tokens

        elif token == "bank" and i + 1 < len(tokens) and tokens[i + 1] == "balance":
            synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]
            augmented_tokens.append(random.choice(synonyms_for_balance))
            if i + 2 < len(tokens) and tokens[i + 2] == "$":
                augmented_tokens.append("$")
                random_amount = f"{random.randint(1, 10_000):,}"
                augmented_tokens.append(random_amount)
                i += 3  # Skip "bank", "balance", and "$"
            else:
                i += 2

        elif token == "$":
            augmented_tokens.append(token)
            random_amount = f"{random.randint(1, 10_000):,}"
            augmented_tokens.append(random_amount)
            i += 1

        elif token in ['.']:
            augmented_tokens.append(token)
        
        else:
            augmented_tokens.append(token)
        
        i += 1

    # Ensure the final token '.' is included if it exists in the original tokens
    if tokens[-1] == '.':
        augmented_tokens.append('.')

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield', 'owner', 'Alex', 'Johnson', 'bank balance', '$', '2,500', 'birthday', 'March 15 1990','.']
original_labels = ['T4-T1', 'T1-St', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Bi', 'O']

# Generate and save augmented sentences
output_file = 'E_1.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

############################################################################################2
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Function to replace grouped tokens with augmented ones using Faker
def augment_sentence(tokens):
    # Define replacement terms
    living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
    synonyms_for_owner = ['possessor', 'owner', 'proprietor']  # Synonyms list
    synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }
    
    augmented_tokens = []
    i = 0
    while i < len(tokens):
        # Replace 'living' with a random term from living_terms
        if tokens[i] == 'living':
            augmented_tokens.append(random.choice(living_terms))  # Add a random living term
            if i + 4 < len(tokens):  # Generate a complete address if enough tokens remain
                building_number = fake.building_number()
                street_name = fake.word()  # Generate a single-word street name
                street_type = tokens[i + 3]  # Keep original street type (e.g., "St", "Ave")
                city = fake.word()  # Generate a single-word city name
                augmented_tokens.append(f"{building_number} {street_name} {street_type} {city}")
                i += 5  # Skip next four tokens (number, street name, street type, city)
            else:
                i += 1

        # Replace 'bank balance' with a random synonym and a random dollar amount
        elif tokens[i] == "bank" and i + 1 < len(tokens) and tokens[i + 1] == "balance":
            augmented_tokens.append(random.choice(synonyms_for_balance))  # Add a synonym for balance
            if i + 2 < len(tokens) and tokens[i + 2] == "$":  # Check if '$' follows
                augmented_tokens.append("$")  # Add the dollar sign
                random_amount = f"{random.randint(1, 10_000):,}"  # Generate a random amount
                augmented_tokens.append(random_amount)  # Add the random money amount
                i += 4  # Skip 'bank', 'balance', and '$'
            else:
                i += 2  # Skip 'bank' and 'balance' only if '$' isn't present

        # Generate a complete birthday token if 'birthday' found
        elif tokens[i] == 'birthday':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            augmented_tokens.append(tokens[i])  # Append 'birthday' token
            augmented_tokens.append(f"{random_month} {day} {year}")  # Append full date
            i += 4  # Skip the next three tokens (original month, day, year)

        # Replace 'owner' with a random synonym and unique names
        elif tokens[i] == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Add a synonym for owner
            augmented_tokens.append(get_unique_first_name())  # Append unique first name
            augmented_tokens.append(get_unique_last_name())   # Append unique last name
            i += 1  # Move past the 'owner' token
            # Skip over any original names
            while i < len(tokens) and tokens[i] not in ['.', 'birthday', 'living', 'bank']:
                i += 1  # Skip original names until a non-name token is found

        # Keep all other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
            i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['birthday', 'March', '15', '1990', 'bank', 'balance', '$', '2,500', 'living', '123', 'Maple', 'St', 'Springfield', 'owner', 'Alex', 'Johnson', '.']
original_labels = ['T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-St', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_2.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###########################################################################################################3
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Living terms and synonyms for balance
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary to map months to the maximum days
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }

    i = 0
    while i < len(tokens):
        # Replace first name with a unique random first name
        if tokens[i] == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        
        # Replace last name with a unique random last name
        elif tokens[i] == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        # Generate a complete birthday token if 'birthday' found
        elif tokens[i] == 'birthday':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            augmented_tokens.append(tokens[i])  # Append 'birthday' token
            augmented_tokens.append(f"{random_month} {day} {year}")  # Append full date
            i += 4  # Move past the next three tokens (original month, day, year)
            continue  # Skip the rest of the loop for this iteration
        
        # Generate a complete address if 'living' found
        elif tokens[i] == 'living' and i + 4 < len(tokens):
            augmented_tokens.append(random.choice(living_terms))  # Replace with a random living term
            building_number = fake.building_number()
            street_name = fake.word()  # Generate a single-word street name
            street_type = tokens[i + 3]  # Keep original street type (e.g., "St", "Ave")
            city = fake.word()  # Generate a single-word city name
            augmented_tokens.append(f"{building_number} {street_name} {street_type} {city}")
            i += 5  # Skip next four tokens (number, street name, street type, city)
            continue  # Skip the rest of the loop for this iteration
        
        # Replace balance-related terms with synonyms
        elif tokens[i] in synonyms_for_balance:
            augmented_tokens.append(random.choice(synonyms_for_balance))  # Replace with a random synonym
        
        # Replace the amount of money if '$' is found
        elif tokens[i] == '$':
            amount = tokens[i + 1]  # Get the amount (next token after '$')
            new_amount = random.randint(1000, 10000)  # Generate a new random amount
            augmented_tokens.append('$')  # Keep the dollar sign
            augmented_tokens.append(f"{new_amount:,}")  # Add the new amount with formatting (e.g., '5,200')
            i += 2  # Skip the next token (the old amount)
            continue  # Skip the rest of the loop for this iteration
        
        # Keep other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
        
        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['Alex', 'Johnson', 'bank balance', '$', '2,500', 'living', '123', 'Maple', 'St', 'Springfield', 'birthday', 'March', '15', '1990', '.']
original_labels = ['T1-Na', 'T1-La', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-St','T4-T1', 'T1-Bi', 'O']

# Generate and save augmented sentences
output_file = 'E_3.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

####################################################4
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Word replacement lists
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Helper functions to get unique names
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Function to augment sentence by replacing tokens
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary for month-day mapping
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }
    
    is_address = False
    skip_next_tokens = False  # Flag to skip address and birthday parts

    for i, token in enumerate(tokens):
        # Skip tokens after address or birthday has been added
        if skip_next_tokens:
            if token in ['Maple', 'St', 'Springfield', 'March', '15', '1990']:
                continue
            skip_next_tokens = False  # Reset flag

        # Replace specific tokens
        if token == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        elif token == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        elif token == 'living':
            is_address = True  # Start of address
            augmented_tokens.append(random.choice(living_terms))  # Replace 'living' with a random term
        elif is_address and token.isdigit() and tokens[i - 1] == 'living':
            street_name = fake.street_name().split()[0]  # Single-word street
            city_name = fake.city().split()[0]  # Single-word city
            address = f"{fake.building_number()} {street_name} {random.choice(['St', 'Ave', 'Blvd', 'Rd'])} {city_name}"
            augmented_tokens.append(address)
            is_address = False  # End address
            skip_next_tokens = True
        
        elif token == 'birthday':
            random_month = random.choice(list(month_days.keys()))
            random_day = random.randint(1, month_days[random_month])
            random_year = random.randint(1980, 2020)
            birthday = f"{random_month} {random_day} {random_year}"
            augmented_tokens.append('birthday')
            augmented_tokens.append(birthday)
            skip_next_tokens = True
        
        elif token == '$':
            augmented_tokens.append(token)  # Keep dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace amount
        
        else:
            if not is_address:  # Skip tokens included in address
                # Word replacement for balance-related terms
                if token in synonyms_for_balance:
                    token = random.choice(synonyms_for_balance)
                augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = [
    'Alex', 'Johnson', 'living', '123', 'Maple', 'St', 'Springfield', 
    'birthday', 'March', '15', '1990', 'bank balance', '$', '2,500', '.'
]
original_labels = ['T1-Na', 'T1-La', 'T4-T1', 'T1-St', 'T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'O']

# Generate and save augmented sentences
output_file = 'E_4.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

####################################################################5
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Define lists for word replacements
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary to map months to the maximum days
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }

    i = 0
    while i < len(tokens):
        # Handle address with any term from living_terms
        if tokens[i] in living_terms and i + 4 < len(tokens):
            building_number = fake.building_number()
            street_name = fake.street_name().split()[0]  # Single-word street name
            street_type = tokens[i + 2]  # Use original street type (St, Ave, etc.)
            city = fake.city().split()[0]  # Single-word city name
            full_address = f"{building_number} {street_name} {street_type} {city}"
            augmented_tokens.append(random.choice(living_terms))  # Randomly replace with term from living_terms
            augmented_tokens.append(full_address)  # Address as single token
            i += 4  # Skip to next token after address components
        
        # Replace first and last names using unique generators
        elif tokens[i] == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        elif tokens[i] == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        # Replace dollar amounts
        elif tokens[i] == '$':
            augmented_tokens.append(tokens[i])
        elif tokens[i].replace(',', '').isdigit() and i > 0 and tokens[i-1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))
        
        # Replace "owner" with synonyms
        elif tokens[i] == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))
        
        # Replace balance-related terms with synonyms
        elif tokens[i] in synonyms_for_balance:
            augmented_tokens.append(random.choice(synonyms_for_balance))
        
        # Combine tokens to create a complete birthday if "birthday" is detected
        elif tokens[i] == 'birthday':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            birthday = f"{random_month} {day} {year}"
            augmented_tokens.append(tokens[i])  # Keep 'birthday'
            augmented_tokens.append(birthday)  # Append full date as single token
            i += 3  # Skip to next token after date components
        
        # Keep other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
        
        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = [
    'living', '123', 'Maple', 'St', 'Springfield', 
    'birthday', 'March', '15', '1990', 
    'bank balance', '$', '2,500', 
    'owner', 'Alex', 'Johnson', '.'
]
original_labels = ['T4-T1', 'T1-St', 'T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_5.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###################################################################################################6
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Define lists for word replacements
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary to map months to the maximum days
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }

    i = 0
    while i < len(tokens):
        # Handle address with any term from living_terms
        if tokens[i] in living_terms and i + 4 < len(tokens):
            building_number = fake.building_number()
            street_name = fake.street_name().split()[0]  # Single-word street name
            street_type = tokens[i + 2]  # Use original street type (St, Ave, etc.)
            city = fake.city().split()[0]  # Single-word city name
            full_address = f"{building_number} {street_name} {street_type} {city}"
            augmented_tokens.append(random.choice(living_terms))  # Randomly replace with term from living_terms
            augmented_tokens.append(full_address)  # Address as single token
            i += 4  # Skip to next token after address components
        
        # Replace first and last names using unique generators
        elif tokens[i] == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        elif tokens[i] == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        # Replace dollar amounts
        elif tokens[i] == '$':
            augmented_tokens.append(tokens[i])
        elif tokens[i].replace(',', '').isdigit() and i > 0 and tokens[i-1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))
        
        # Replace "owner" with synonyms
        elif tokens[i] == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))
        
        # Replace balance-related terms with synonyms
        elif tokens[i] in synonyms_for_balance:
            augmented_tokens.append(random.choice(synonyms_for_balance))
        
        # Combine tokens to create a complete birthday if "birthday" is detected
        elif tokens[i] == 'birthday':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            birthday = f"{random_month} {day} {year}"
            augmented_tokens.append(tokens[i])  # Keep 'birthday'
            augmented_tokens.append(birthday)  # Append full date as single token
            i += 3  # Skip to next token after date components
        
        # Keep other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
        
        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = [
    'living', '123', 'Maple', 'St', 'Springfield', 
    'birthday', 'March', '15', '1990', 
    'bank balance', '$', '2,500', 
    'owner', 'Alex', 'Johnson', '.'
]
original_labels = ['T4-T1', 'T1-St', 'T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_6.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
########################################################################################################1
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Define lists for word replacements
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary to map months to the maximum days
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }

    i = 0
    while i < len(tokens):
        # Handle address with any term from living_terms
        if tokens[i] in living_terms and i + 4 < len(tokens):
            building_number = fake.building_number()
            street_name = fake.street_name().split()[0]  # Single-word street name
            street_type = tokens[i + 2]  # Use original street type (St, Ave, etc.)
            city = fake.city().split()[0]  # Single-word city name
            full_address = f"{building_number} {street_name} {street_type} {city}"
            augmented_tokens.append(random.choice(living_terms))  # Randomly replace with term from living_terms
            augmented_tokens.append(full_address)  # Address as single token
            i += 4  # Skip to next token after address components
        
        # Replace first and last names using unique generators
        elif tokens[i] == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        elif tokens[i] == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        # Replace dollar amounts
        elif tokens[i] == '$':
            augmented_tokens.append(tokens[i])
        elif tokens[i].replace(',', '').isdigit() and i > 0 and tokens[i-1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))
        
        # Replace "owner" with synonyms
        elif tokens[i] == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))
        
        # Replace balance-related terms with synonyms
        elif tokens[i] in synonyms_for_balance:
            augmented_tokens.append(random.choice(synonyms_for_balance))
        
        elif tokens[i] == 'date birth':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            birthday = f"{random_month} {day} {year}"
            augmented_tokens.append(tokens[i])  # Keep 'date birth'
            augmented_tokens.append(birthday)  # Append full date as single token
            i += 3  # Skip to next token after date components
        
        # Keep other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
        
        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = [
    'living', '123', 'Maple', 'St', 'Springfield', 
    'date birth', 'March', '15', '1990', 
    'bank balance', '$', '2,500', 
    'owner', 'Alex', 'Johnson', '.'
]
original_labels = ['T4-T1', 'T1-St', 'T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_7.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

###########################################################################################################2
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Word replacement lists
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Helper functions to get unique names
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Function to augment sentence by replacing tokens
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary for month-day mapping
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }
    
    is_address = False
    skip_next_tokens = False  # Flag to skip address and birthday parts

    for i, token in enumerate(tokens):
        # Skip tokens after address or birthday has been added
        if skip_next_tokens:
            if token in ['Maple', 'St', 'Springfield', 'March', '15', '1990']:
                continue
            skip_next_tokens = False  # Reset flag

        # Replace specific tokens
        if token == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        elif token == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        elif token == 'living':
            is_address = True  # Start of address
            augmented_tokens.append(random.choice(living_terms))  # Replace 'living' with a random term
        elif is_address and token.isdigit() and tokens[i - 1] == 'living':
            street_name = fake.street_name().split()[0]  # Single-word street
            city_name = fake.city().split()[0]  # Single-word city
            address = f"{fake.building_number()} {street_name} {random.choice(['St', 'Ave', 'Blvd', 'Rd'])} {city_name}"
            augmented_tokens.append(address)
            is_address = False  # End address
            skip_next_tokens = True
        
        elif token == 'date birth':
            random_month = random.choice(list(month_days.keys()))
            random_day = random.randint(1, month_days[random_month])
            random_year = random.randint(1980, 2020)
            birthday = f"{random_month} {random_day} {random_year}"
            augmented_tokens.append('date birth')
            augmented_tokens.append(birthday)
            skip_next_tokens = True
        
        elif token == '$':
            augmented_tokens.append(token)  # Keep dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace amount
        
        else:
            if not is_address:  # Skip tokens included in address
                # Word replacement for balance-related terms
                if token in synonyms_for_balance:
                    token = random.choice(synonyms_for_balance)
                augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = [
    'Alex', 'Johnson', 'living', '123', 'Maple', 'St', 'Springfield', 
    'date birth', 'March', '15', '1990', 'bank balance', '$', '2,500', '.'
]
original_labels = ['T1-Na', 'T1-La', 'T4-T1', 'T1-St', 'T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'O']

# Generate and save augmented sentences
output_file = 'E_8.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
####################################################################################################3
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Living terms and synonyms for balance
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary to map months to the maximum days
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }

    i = 0
    while i < len(tokens):
        # Replace first name with a unique random first name
        if tokens[i] == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        
        # Replace last name with a unique random last name
        elif tokens[i] == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        # Generate a complete birthday token if 'birthday' found
        elif tokens[i] == 'date birth':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            augmented_tokens.append(tokens[i])  # Append 'birthday' token
            augmented_tokens.append(f"{random_month} {day} {year}")  # Append full date
            i += 4  # Move past the next three tokens (original month, day, year)
            continue  # Skip the rest of the loop for this iteration
        
        # Generate a complete address if 'living' found
        elif tokens[i] == 'living' and i + 4 < len(tokens):
            augmented_tokens.append(random.choice(living_terms))  # Replace with a random living term
            building_number = fake.building_number()
            street_name = fake.word()  # Generate a single-word street name
            street_type = tokens[i + 3]  # Keep original street type (e.g., "St", "Ave")
            city = fake.word()  # Generate a single-word city name
            augmented_tokens.append(f"{building_number} {street_name} {street_type} {city}")
            i += 5  # Skip next four tokens (number, street name, street type, city)
            continue  # Skip the rest of the loop for this iteration
        
        # Replace balance-related terms with synonyms
        elif tokens[i] in synonyms_for_balance:
            augmented_tokens.append(random.choice(synonyms_for_balance))  # Replace with a random synonym
        
        # Replace the amount of money if '$' is found
        elif tokens[i] == '$':
            amount = tokens[i + 1]  # Get the amount (next token after '$')
            new_amount = random.randint(1000, 10000)  # Generate a new random amount
            augmented_tokens.append('$')  # Keep the dollar sign
            augmented_tokens.append(f"{new_amount:,}")  # Add the new amount with formatting (e.g., '5,200')
            i += 2  # Skip the next token (the old amount)
            continue  # Skip the rest of the loop for this iteration
        
        # Keep other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
        
        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['Alex', 'Johnson', 'bank balance', '$', '2,500', 'living', '123', 'Maple', 'St', 'Springfield', 'date birth', 'March', '15', '1990', '.']
original_labels = ['T1-Na', 'T1-La', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-St','T4-T1', 'T1-Bi', 'O']

# Generate and save augmented sentences
output_file = 'E_9.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
######################################################################################################4
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Function to replace grouped tokens with augmented ones using Faker
def augment_sentence(tokens):
    # Define replacement terms
    living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
    synonyms_for_owner = ['possessor', 'owner', 'proprietor']  # Synonyms list
    synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }
    
    augmented_tokens = []
    i = 0
    while i < len(tokens):
        # Replace 'living' with a random term from living_terms
        if tokens[i] == 'living':
            augmented_tokens.append(random.choice(living_terms))  # Add a random living term
            if i + 4 < len(tokens):  # Generate a complete address if enough tokens remain
                building_number = fake.building_number()
                street_name = fake.word()  # Generate a single-word street name
                street_type = tokens[i + 3]  # Keep original street type (e.g., "St", "Ave")
                city = fake.word()  # Generate a single-word city name
                augmented_tokens.append(f"{building_number} {street_name} {street_type} {city}")
                i += 5  # Skip next four tokens (number, street name, street type, city)
            else:
                i += 1

        # Replace 'bank balance' with a random synonym and a random dollar amount
        elif tokens[i] == "bank" and i + 1 < len(tokens) and tokens[i + 1] == "balance":
            augmented_tokens.append(random.choice(synonyms_for_balance))  # Add a synonym for balance
            if i + 2 < len(tokens) and tokens[i + 2] == "$":  # Check if '$' follows
                augmented_tokens.append("$")  # Add the dollar sign
                random_amount = f"{random.randint(1, 10_000):,}"  # Generate a random amount
                augmented_tokens.append(random_amount)  # Add the random money amount
                i += 4  # Skip 'bank', 'balance', and '$'
            else:
                i += 2  # Skip 'bank' and 'balance' only if '$' isn't present

        # Generate a complete birthday token if 'birthday' found
        elif tokens[i] == 'date birth':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            augmented_tokens.append(tokens[i])  # Append 'birthday' token
            augmented_tokens.append(f"{random_month} {day} {year}")  # Append full date
            i += 4  # Skip the next three tokens (original month, day, year)

        # Replace 'owner' with a random synonym and unique names
        elif tokens[i] == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Add a synonym for owner
            augmented_tokens.append(get_unique_first_name())  # Append unique first name
            augmented_tokens.append(get_unique_last_name())   # Append unique last name
            i += 1  # Move past the 'owner' token
            # Skip over any original names
            while i < len(tokens) and tokens[i] not in ['.', 'birthday', 'living', 'bank']:
                i += 1  # Skip original names until a non-name token is found

        # Keep all other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
            i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['date birth', 'March', '15', '1990', 'bank', 'balance', '$', '2,500', 'living', '123', 'Maple', 'St', 'Springfield', 'owner', 'Alex', 'Johnson', '.']
original_labels = ['T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-St', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_10.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#################################################################################################5
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    # Randomly replace "living" with one of the given terms
    living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
    augmented_tokens = [random.choice(living_terms)]  # Start with a random term

    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }
    
    i = 1  # Start from the second token since "living" is already added
    while i < len(tokens):
        token = tokens[i]
        
        # Replace street address tokens after "Living"
        if token.isdigit() and tokens[i-1] == "living":
            # Generate a simplified address with single-word street name and city
            building_number = fake.building_number()
            street_name = fake.word().capitalize()  # Single word for street name
            city = fake.city().split()[0]  # Single word for city
            street_address = f"{building_number} {street_name} St {city}"
            augmented_tokens.append(street_address)
            i += 4  # Skip the next 4 tokens that make up the full address in the original tokens
            
            # Add "owner" after the street address and generate random name and surname
            synonyms_for_owner = ['possessor', 'owner', 'proprietor']  # Synonyms list
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Add a random synonym for "owner"
            augmented_tokens.append(get_unique_first_name())  # Unique first name
            augmented_tokens.append(get_unique_last_name())   # Unique last name
            i += 2  # Skip the name and surname tokens in the original tokens
            
        # Handle "birthday" and generate a random date
        elif token == "date birth":
            augmented_tokens.append("date birth")  # Add "birthday" label
            month = random.choice(list(month_days.keys()))
            day = str(random.randint(1, month_days[month]))
            year = str(random.randint(1980, 2020))
            birthday = f"{month} {day} {year}"
            augmented_tokens.append(birthday)
            i += 3  # Skip the next 3 tokens that make up the date in the original tokens

        # Replace "bank balance" with a random synonym
        elif token == "bank" and i + 1 < len(tokens) and tokens[i + 1] == "balance":
            synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]
            augmented_tokens.append(random.choice(synonyms_for_balance))
            if i + 2 < len(tokens) and tokens[i + 2] == "$":  # Check if '$' follows
                augmented_tokens.append("$")  # Add the dollar sign
                random_amount = f"{random.randint(1, 10_000):,}"  # Generate a random amount with commas
                augmented_tokens.append(random_amount)  # Add the random money amount
                i += 3  # Skip "bank", "balance", and "$"
            else:
                i += 2  # Skip "bank" and "balance" only if '$' isn't present

        # Handle "$" (money amounts) if it's standalone
        elif token == "$":
            augmented_tokens.append(token)  # Add the dollar sign
            random_amount = f"{random.randint(1, 10_000):,}"  # Generate a random amount with commas
            augmented_tokens.append(random_amount)  # Add the random money amount
            i += 1  # Skip the original amount in the tokens

        # Keep specific tokens like "."
        elif token in ['.']:
            augmented_tokens.append(token)
        
        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)
        
        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield', 'owner', 'Alex', 'Johnson', 'bank', 'balance', '$', '2,500', 'date birth', 'March', '15', '1990', '.']
original_labels = ['T4-T1', 'T1-St', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Bi', 'O']

# Generate and save augmented sentences
output_file = 'E_11.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
########################################################################6
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Define lists for word replacements
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary to map months to the maximum days
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }

    i = 0
    while i < len(tokens):
        # Handle address with any term from living_terms
        if tokens[i] in living_terms and i + 4 < len(tokens):
            building_number = fake.building_number()
            street_name = fake.street_name().split()[0]  # Single-word street name
            street_type = tokens[i + 2]  # Use original street type (St, Ave, etc.)
            city = fake.city().split()[0]  # Single-word city name
            full_address = f"{building_number} {street_name} {street_type} {city}"
            augmented_tokens.append(random.choice(living_terms))  # Randomly replace with term from living_terms
            augmented_tokens.append(full_address)  # Address as single token
            i += 4  # Skip to next token after address components
        
        # Replace first and last names using unique generators
        elif tokens[i] == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        elif tokens[i] == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        # Replace dollar amounts
        elif tokens[i] == '$':
            augmented_tokens.append(tokens[i])
        elif tokens[i].replace(',', '').isdigit() and i > 0 and tokens[i-1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))
        
        # Replace "owner" with synonyms
        elif tokens[i] == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))
        
        # Replace balance-related terms with synonyms
        elif tokens[i] in synonyms_for_balance:
            augmented_tokens.append(random.choice(synonyms_for_balance))
        
        # Combine tokens to create a complete birthday if "birthday" is detected
        elif tokens[i] == 'date birth':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            birthday = f"{random_month} {day} {year}"
            augmented_tokens.append(tokens[i])  # Keep 'birthday'
            augmented_tokens.append(birthday)  # Append full date as single token
            i += 3  # Skip to next token after date components
        
        # Keep other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
        
        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = [
    'living', '123', 'Maple', 'St', 'Springfield', 
    'date birth', 'March', '15', '1990', 
    'bank balance', '$', '2,500', 
    'owner', 'Alex', 'Johnson', '.'
]
original_labels = ['T4-T1', 'T1-St', 'T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_12.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#######################################################################################################1
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Function to replace grouped tokens with augmented ones using Faker
def augment_sentence(tokens):
    # Define replacement terms
    living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
    synonyms_for_owner = ['possessor', 'owner', 'proprietor']  # Synonyms list
    synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }
    
    augmented_tokens = []
    i = 0
    while i < len(tokens):
        # Replace 'living' with a random term from living_terms
        if tokens[i] == 'living':
            augmented_tokens.append(random.choice(living_terms))  # Add a random living term
            if i + 4 < len(tokens):  # Generate a complete address if enough tokens remain
                building_number = fake.building_number()
                street_name = fake.word()  # Generate a single-word street name
                street_type = tokens[i + 3]  # Keep original street type (e.g., "St", "Ave")
                city = fake.word()  # Generate a single-word city name
                augmented_tokens.append(f"{building_number} {street_name} {street_type} {city}")
                i += 5  # Skip next four tokens (number, street name, street type, city)
            else:
                i += 1

        # Replace 'bank balance' with a random synonym and a random dollar amount
        elif tokens[i] == "bank" and i + 1 < len(tokens) and tokens[i + 1] == "balance":
            augmented_tokens.append(random.choice(synonyms_for_balance))  # Add a synonym for balance
            if i + 2 < len(tokens) and tokens[i + 2] == "$":  # Check if '$' follows
                augmented_tokens.append("$")  # Add the dollar sign
                random_amount = f"{random.randint(1, 10_000):,}"  # Generate a random amount
                augmented_tokens.append(random_amount)  # Add the random money amount
                i += 4  # Skip 'bank', 'balance', and '$'
            else:
                i += 2  # Skip 'bank' and 'balance' only if '$' isn't present

        # Generate a complete birthday token if 'birthday' found
        elif tokens[i] == 'born':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            augmented_tokens.append(tokens[i])  # Append 'birthday' token
            augmented_tokens.append(f"{random_month} {day} {year}")  # Append full date
            i += 4  # Skip the next three tokens (original month, day, year)

        # Replace 'owner' with a random synonym and unique names
        elif tokens[i] == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Add a synonym for owner
            augmented_tokens.append(get_unique_first_name())  # Append unique first name
            augmented_tokens.append(get_unique_last_name())   # Append unique last name
            i += 1  # Move past the 'owner' token
            # Skip over any original names
            while i < len(tokens) and tokens[i] not in ['.', 'birthday', 'living', 'bank']:
                i += 1  # Skip original names until a non-name token is found

        # Keep all other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
            i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['born', 'March', '15', '1990', 'bank', 'balance', '$', '2,500', 'living', '123', 'Maple', 'St', 'Springfield', 'owner', 'Alex', 'Johnson', '.']
original_labels = ['T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-St', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_13.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
########################################################################################################2
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    # Randomly replace "living" with one of the given terms
    living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
    augmented_tokens = [random.choice(living_terms)]  # Start with a random term

    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }
    
    i = 1  # Start from the second token since "living" is already added
    while i < len(tokens):
        token = tokens[i]
        
        # Replace street address tokens after "Living"
        if token.isdigit() and tokens[i-1] == "living":
            # Generate a simplified address with single-word street name and city
            building_number = fake.building_number()
            street_name = fake.word().capitalize()  # Single word for street name
            city = fake.city().split()[0]  # Single word for city
            street_address = f"{building_number} {street_name} St {city}"
            augmented_tokens.append(street_address)
            i += 4  # Skip the next 4 tokens that make up the full address in the original tokens
            
            # Add "owner" after the street address and generate random name and surname
            synonyms_for_owner = ['possessor', 'owner', 'proprietor']  # Synonyms list
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Add a random synonym for "owner"
            augmented_tokens.append(get_unique_first_name())  # Unique first name
            augmented_tokens.append(get_unique_last_name())   # Unique last name
            i += 2  # Skip the name and surname tokens in the original tokens
            
        # Handle "birthday" and generate a random date
        elif token == "born":
            augmented_tokens.append("born")  # Add "birthday" label
            month = random.choice(list(month_days.keys()))
            day = str(random.randint(1, month_days[month]))
            year = str(random.randint(1980, 2020))
            birthday = f"{month} {day} {year}"
            augmented_tokens.append(birthday)
            i += 3  # Skip the next 3 tokens that make up the date in the original tokens

        # Replace "bank balance" with a random synonym
        elif token == "bank" and i + 1 < len(tokens) and tokens[i + 1] == "balance":
            synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]
            augmented_tokens.append(random.choice(synonyms_for_balance))
            if i + 2 < len(tokens) and tokens[i + 2] == "$":  # Check if '$' follows
                augmented_tokens.append("$")  # Add the dollar sign
                random_amount = f"{random.randint(1, 10_000):,}"  # Generate a random amount with commas
                augmented_tokens.append(random_amount)  # Add the random money amount
                i += 3  # Skip "bank", "balance", and "$"
            else:
                i += 2  # Skip "bank" and "balance" only if '$' isn't present

        # Handle "$" (money amounts) if it's standalone
        elif token == "$":
            augmented_tokens.append(token)  # Add the dollar sign
            random_amount = f"{random.randint(1, 10_000):,}"  # Generate a random amount with commas
            augmented_tokens.append(random_amount)  # Add the random money amount
            i += 1  # Skip the original amount in the tokens

        # Keep specific tokens like "."
        elif token in ['.']:
            augmented_tokens.append(token)
        
        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)
        
        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield', 'owner', 'Alex', 'Johnson', 'bank', 'balance', '$', '2,500', 'born', 'March', '15', '1990', '.']
original_labels = ['T4-T1', 'T1-St', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Bi', 'O']

# Generate and save augmented sentences
output_file = 'E_14.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

##################################################################################################3
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Function to replace grouped tokens with augmented ones using Faker
def augment_sentence(tokens):
    # Define replacement terms
    living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
    synonyms_for_owner = ['possessor', 'owner', 'proprietor']  # Synonyms list
    synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }
    
    augmented_tokens = []
    i = 0
    while i < len(tokens):
        # Replace 'living' with a random term from living_terms
        if tokens[i] == 'living':
            augmented_tokens.append(random.choice(living_terms))  # Add a random living term
            if i + 4 < len(tokens):  # Generate a complete address if enough tokens remain
                building_number = fake.building_number()
                street_name = fake.word()  # Generate a single-word street name
                street_type = tokens[i + 3]  # Keep original street type (e.g., "St", "Ave")
                city = fake.word()  # Generate a single-word city name
                augmented_tokens.append(f"{building_number} {street_name} {street_type} {city}")
                i += 5  # Skip next four tokens (number, street name, street type, city)
            else:
                i += 1

        # Replace 'bank balance' with a random synonym and a random dollar amount
        elif tokens[i] == "bank" and i + 1 < len(tokens) and tokens[i + 1] == "balance":
            augmented_tokens.append(random.choice(synonyms_for_balance))  # Add a synonym for balance
            if i + 2 < len(tokens) and tokens[i + 2] == "$":  # Check if '$' follows
                augmented_tokens.append("$")  # Add the dollar sign
                random_amount = f"{random.randint(1, 10_000):,}"  # Generate a random amount
                augmented_tokens.append(random_amount)  # Add the random money amount
                i += 4  # Skip 'bank', 'balance', and '$'
            else:
                i += 2  # Skip 'bank' and 'balance' only if '$' isn't present

        # Generate a complete birthday token if 'birthday' found
        elif tokens[i] == 'born':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            augmented_tokens.append(tokens[i])  # Append 'birthday' token
            augmented_tokens.append(f"{random_month} {day} {year}")  # Append full date
            i += 4  # Skip the next three tokens (original month, day, year)

        # Replace 'owner' with a random synonym and unique names
        elif tokens[i] == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Add a synonym for owner
            augmented_tokens.append(get_unique_first_name())  # Append unique first name
            augmented_tokens.append(get_unique_last_name())   # Append unique last name
            i += 1  # Move past the 'owner' token
            # Skip over any original names
            while i < len(tokens) and tokens[i] not in ['.', 'born', 'living', 'bank']:
                i += 1  # Skip original names until a non-name token is found

        # Keep all other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
            i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['born', 'March', '15', '1990', 'bank', 'balance', '$', '2,500', 'living', '123', 'Maple', 'St', 'Springfield', 'owner', 'Alex', 'Johnson', '.']
original_labels = ['T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-St', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_15.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

###########################################################################################################4
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Living terms and synonyms for balance
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary to map months to the maximum days
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }

    i = 0
    while i < len(tokens):
        # Replace first name with a unique random first name
        if tokens[i] == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        
        # Replace last name with a unique random last name
        elif tokens[i] == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        # Generate a complete birthday token if 'birthday' found
        elif tokens[i] == 'born':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            augmented_tokens.append(tokens[i])  # Append 'birthday' token
            augmented_tokens.append(f"{random_month} {day} {year}")  # Append full date
            i += 4  # Move past the next three tokens (original month, day, year)
            continue  # Skip the rest of the loop for this iteration
        
        # Generate a complete address if 'living' found
        elif tokens[i] == 'living' and i + 4 < len(tokens):
            augmented_tokens.append(random.choice(living_terms))  # Replace with a random living term
            building_number = fake.building_number()
            street_name = fake.word()  # Generate a single-word street name
            street_type = tokens[i + 3]  # Keep original street type (e.g., "St", "Ave")
            city = fake.word()  # Generate a single-word city name
            augmented_tokens.append(f"{building_number} {street_name} {street_type} {city}")
            i += 5  # Skip next four tokens (number, street name, street type, city)
            continue  # Skip the rest of the loop for this iteration
        
        # Replace balance-related terms with synonyms
        elif tokens[i] in synonyms_for_balance:
            augmented_tokens.append(random.choice(synonyms_for_balance))  # Replace with a random synonym
        
        # Replace the amount of money if '$' is found
        elif tokens[i] == '$':
            amount = tokens[i + 1]  # Get the amount (next token after '$')
            new_amount = random.randint(1000, 10000)  # Generate a new random amount
            augmented_tokens.append('$')  # Keep the dollar sign
            augmented_tokens.append(f"{new_amount:,}")  # Add the new amount with formatting (e.g., '5,200')
            i += 2  # Skip the next token (the old amount)
            continue  # Skip the rest of the loop for this iteration
        
        # Keep other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
        
        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['Alex', 'Johnson', 'bank balance', '$', '2,500', 'living', '123', 'Maple', 'St', 'Springfield', 'born', 'March', '15', '1990', '.']
original_labels = ['T1-Na', 'T1-La', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-St','T4-T1', 'T1-Bi', 'O']

# Generate and save augmented sentences
output_file = 'E_16.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###################################################################################5
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Word replacement lists
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Helper functions to get unique names
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Function to augment sentence by replacing tokens
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary for month-day mapping
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }
    
    is_address = False
    skip_next_tokens = False  # Flag to skip address and birthday parts

    for i, token in enumerate(tokens):
        # Skip tokens after address or birthday has been added
        if skip_next_tokens:
            if token in ['Maple', 'St', 'Springfield', 'March', '15', '1990']:
                continue
            skip_next_tokens = False  # Reset flag

        # Replace specific tokens
        if token == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        elif token == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        elif token == 'living':
            is_address = True  # Start of address
            augmented_tokens.append(random.choice(living_terms))  # Replace 'living' with a random term
        elif is_address and token.isdigit() and tokens[i - 1] == 'living':
            street_name = fake.street_name().split()[0]  # Single-word street
            city_name = fake.city().split()[0]  # Single-word city
            address = f"{fake.building_number()} {street_name} {random.choice(['St', 'Ave', 'Blvd', 'Rd'])} {city_name}"
            augmented_tokens.append(address)
            is_address = False  # End address
            skip_next_tokens = True
        
        elif token == 'born':
            random_month = random.choice(list(month_days.keys()))
            random_day = random.randint(1, month_days[random_month])
            random_year = random.randint(1980, 2020)
            birthday = f"{random_month} {random_day} {random_year}"
            augmented_tokens.append('born')
            augmented_tokens.append(birthday)
            skip_next_tokens = True
        
        elif token == '$':
            augmented_tokens.append(token)  # Keep dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace amount
        
        else:
            if not is_address:  # Skip tokens included in address
                # Word replacement for balance-related terms
                if token in synonyms_for_balance:
                    token = random.choice(synonyms_for_balance)
                augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = [
    'Alex', 'Johnson', 'living', '123', 'Maple', 'St', 'Springfield', 
    'born', 'March', '15', '1990', 'bank balance', '$', '2,500', '.'
]
original_labels = ['T1-Na', 'T1-La', 'T4-T1', 'T1-St', 'T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'O']

# Generate and save augmented sentences
output_file = 'E_17.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
####################################################################################6
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Predefined sets to store unique first and last names
unique_first_names = set()
unique_last_names = set()

# Helper functions to get a unique first or last name
def get_unique_first_name():
    while True:
        first_name = fake.first_name()
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            return first_name

def get_unique_last_name():
    while True:
        last_name = fake.last_name()
        if last_name not in unique_last_names:
            unique_last_names.add(last_name)
            return last_name

# Define lists for word replacements
living_terms = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_balance = ["bank balance", "savings", "funds", "capital", "wealth", "balance", "assets", "money", "income", "equity", "liabilities"]

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens):
    augmented_tokens = []
    
    # Dictionary to map months to the maximum days
    month_days = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }

    i = 0
    while i < len(tokens):
        # Handle address with any term from living_terms
        if tokens[i] in living_terms and i + 4 < len(tokens):
            building_number = fake.building_number()
            street_name = fake.street_name().split()[0]  # Single-word street name
            street_type = tokens[i + 2]  # Use original street type (St, Ave, etc.)
            city = fake.city().split()[0]  # Single-word city name
            full_address = f"{building_number} {street_name} {street_type} {city}"
            augmented_tokens.append(random.choice(living_terms))  # Randomly replace with term from living_terms
            augmented_tokens.append(full_address)  # Address as single token
            i += 4  # Skip to next token after address components
        
        # Replace first and last names using unique generators
        elif tokens[i] == 'Alex':
            augmented_tokens.append(get_unique_first_name())
        elif tokens[i] == 'Johnson':
            augmented_tokens.append(get_unique_last_name())
        
        # Replace dollar amounts
        elif tokens[i] == '$':
            augmented_tokens.append(tokens[i])
        elif tokens[i].replace(',', '').isdigit() and i > 0 and tokens[i-1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))
        
        # Replace "owner" with synonyms
        elif tokens[i] == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))
        
        # Replace balance-related terms with synonyms
        elif tokens[i] in synonyms_for_balance:
            augmented_tokens.append(random.choice(synonyms_for_balance))
        
        # Combine tokens to create a complete birthday if "birthday" is detected
        elif tokens[i] == 'born':
            random_month = random.choice(list(month_days.keys()))
            day = random.randint(1, month_days[random_month])
            year = random.randint(1980, 2020)
            birthday = f"{random_month} {day} {year}"
            augmented_tokens.append(tokens[i])  # Keep 'birthday'
            augmented_tokens.append(birthday)  # Append full date as single token
            i += 3  # Skip to next token after date components
        
        # Keep other tokens unchanged
        else:
            augmented_tokens.append(tokens[i])
        
        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=10):
    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = [
    'living', '123', 'Maple', 'St', 'Springfield', 
    'born', 'March', '15', '1990', 
    'bank balance', '$', '2,500', 
    'owner', 'Alex', 'Johnson', '.'
]
original_labels = ['T4-T1', 'T1-St', 'T4-T1', 'T1-Bi', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_18.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#############################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for "owner," "IP address," and "SSN"
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']

# Function to augment sentence tokens with SSN, name, IP address, and owner synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['SSN', '123-45-6789', 'IP address', '192.168.1.1', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T1', 'T1-Ss', 'T4-T3', 'T3-Ip', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_19.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#################################################################################################

from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for "owner," "IP address," and "SSN"
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialecuritynumber', 'IDnumber']

# Function to augment sentence tokens with SSN, name, IP address, and owner synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1', 'SSN', '123-45-6789', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip', 'T4-T1', 'T1-Ss', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_20.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

##########################################################################################################

from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for "IP address" and "SSN"
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']

# Function to augment sentence tokens with SSN, name, and IP address changes
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value after 'SSN' with a synonym and generate new SSN
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value with a synonym and generate a new IP
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['Emily', 'Smith', 'IP address', '192.168.1.1', 'SSN', '123-45-6789', '.']
original_labels = ['T1-Na', 'T1-La', 'T4-T3', 'T3-Ip', 'T4-T1', 'T1-Ss', 'O']

# Generate and save augmented sentences
output_file = 'E_21.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##########################################################################################################credit
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVV', 'CVC', 'CVV2','cardverificationcode']

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace credit card with a synonym and add a random credit card number
        if token == 'credit card':
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
            credit_card_num = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_num)  # Add the generated card number
        # Replace security code with a synonym and generate a security code
        elif token == 'securitycode':
            augmented_tokens.append(random.choice(synonyms_for_security_code))
            security_code = fake.credit_card_security_code()  # Generate a random security code (CVV)
            augmented_tokens.append(security_code)  # Add the generated security code
        # Skip the token '12334555' as it's redundant
        elif token == '3530567226316942':
            continue  # Do not append it to augmented_tokens
        # Replace charge with a synonym
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))
        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email with a synonym
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"

            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner with a synonym
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))
        # Replace specific first and last names uniquely
        elif token == 'Emily':  # First name specific to the example
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Williams':  # Last name specific to the example
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Otherwise, don't add the original token if it's already been replaced
        elif token.isdigit() and token != '12334555':  # Avoid numeric values like the security code and credit card number
            continue  # Skip the original numeric values like '3530567226316942' or '123'
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Helper functions to ensure unique names
def get_unique_first_name(used_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

def get_unique_last_name(used_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942', 'securitycode', '123', 'charge', '$', '150', 'email', 'alex.johnson@gmail.com', 'owner', 'Emily', 'Williams', '.']
original_labels = ['T4-T2', 'T2-credit','T4-T2', 'T2-Secode','T4-T2','T4-T2', 'T2-Mo', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_22.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)


####################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']

# Function to generate a unique name from a unified set
def get_unique_name(used_names, name_type='first'):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        if name_type == 'first':
            new_name = fake.first_name()
        else:
            new_name = fake.last_name()
        
        if new_name not in used_names:
            return new_name
        attempts += 1
    # Fallback to just generating a random name if unique not found
    return fake.first_name() if name_type == 'first' else fake.last_name()

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email-related tokens
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with a random synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                domain = random.choice(['gmail.com', 'yahoo.com'])
            else:
                domain = fake.domain_name()  # Use a random domain from Faker
            
            # Ensure unique names for emails
            new_first_name = get_unique_name(used_first_names, name_type='first')
            used_first_names.add(new_first_name)

            new_last_name = get_unique_name(used_last_names, name_type='last')
            used_last_names.add(new_last_name)

            augmented_tokens.append(f"{new_first_name.lower()}.{new_last_name.lower()}@{domain}")  # Replace with random email
        # Replace owner-related tokens
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with a random synonym
        elif token == 'Emily':  # First name specific to the example
            new_first_name = get_unique_name(used_first_names, name_type='first')
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Williams':  # Last name specific to the example
            new_last_name = get_unique_name(used_last_names, name_type='last')
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace charge-related tokens
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with a random synonym
        # Replace credit card-related tokens and number
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with a random synonym
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code-related tokens
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with a random synonym
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@gmail.com', 'owner', 'Emily', 'Williams', 'credit card','3530567226316942','securitycode', '123', 'charge', '$', '150', '.']
original_labels = ['T4-T3', 'T3-Em', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T2', 'T2-credit','T4-T2', 'T2-Secode','T4-T2', 'T4-T2', 'T2-Mo', 'O']

# Generate and save augmented sentences
output_file = 'E_23.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942', 'securitycode', '123', 'charge', '$', '150', 'owner', 'Emily', 'Williams', 'email', 'alex.johnson@email.com', '.']
original_labels = ['T4-T2', 'T2-credit','T4-T2', 'T2-Secode','T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T3', 'T3-Em', 'O']

# Generate and save augmented sentences
output_file = 'E_24.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#####################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email synonyms or emails
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with a synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with generated email
        # Replace charge synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with a synonym
        # Replace credit card synonyms and generate fake credit card number
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with a synonym
        elif token.replace(' ', '').isdigit() and len(token) == 16:  # Credit card number
            fake_credit_card = fake.credit_card_number(card_type="mastercard")  # Generate a fake credit card number
            augmented_tokens.append(fake_credit_card)
        # Replace security code synonyms and generate fake security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with a synonym
        elif token.replace(' ', '').isdigit() and len(token) == 3:  # CVV / security code
            fake_security_code = fake.credit_card_security_code(card_type="mastercard")  # Generate a fake security code
            augmented_tokens.append(fake_security_code)
        # Replace the owner and corresponding names
        elif token == 'Emily':  # First name specific to the example
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Williams':  # Last name specific to the example
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['Emily', 'Williams', 'email', 'alex.johnson@email.com', 'credit card','3530567226316942', 'securitycode', '123','charge', '$', '150', '.']
original_labels = ['T1-Na', 'T1-La', 'T4-T3', 'T3-Em', 'T4-T2', 'T2-credit','T4-T2', 'T2-Secode','T4-T2', 'T4-T2', 'T2-Mo','O']

# Generate and save augmented sentences
output_file = 'E_25.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']

# Function to augment SSN, first name, and last name in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Replace SSN synonyms or SSN values
        if token in synonyms_for_ssn:
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Replace with a synonym
        elif i > 0 and tokens[i-1] in synonyms_for_ssn:  # Replace SSN value after the 'SSN' token
            augmented_tokens.append(fake.ssn())
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with a synonym
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        else:  # Keep other tokens unchanged
            augmented_tokens.append(token)
    
    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['SSN', '899-53-7468', 'owner', 'Douglas', 'Matthew', '.']
original_labels = ['T4-T1', 'T1-Ss', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save 500 augmented sentences
output_file = 'E_26.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

######################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym list for SSN
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']

# Function to augment SSN, first name, and last name in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':  
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Replace with a synonym
        # Replace SSN value following the SSN token
        elif i > 0 and tokens[i-1] in synonyms_for_ssn:  
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        else:  # Keep other tokens unchanged
            augmented_tokens.append(token)
    
    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['Douglas', 'Matthew', 'SSN', '899-53-7468', '.']
original_labels = ['T1-Na', 'T1-La', 'T4-T1', 'T1-Ss', 'O']

# Generate and save 500 augmented sentences
output_file = 'E_27.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

##################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email synonyms or emails
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with a synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with generated email
        # Replace charge synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with a synonym
        # Replace credit card synonyms and generate fake credit card number
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with a synonym
        elif token.replace(' ', '').isdigit() and len(token) == 16:  # Credit card number
            fake_credit_card = fake.credit_card_number(card_type="mastercard")  # Generate a fake credit card number
            augmented_tokens.append(fake_credit_card)
        # Replace security code synonyms and generate fake security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with a synonym
        elif token.replace(' ', '').isdigit() and len(token) == 3:  # CVV / security code
            fake_security_code = fake.credit_card_security_code(card_type="mastercard")  # Generate a fake security code
            augmented_tokens.append(fake_security_code)
        # Replace the owner and corresponding names
        elif token == 'Emily':  # First name specific to the example
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Williams':  # Last name specific to the example
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['Emily', 'Williams','credit card','3530567226316942','email', 'alex.johnson@email.com', 'securitycode', '123','charge', '$', '150', '.']
original_labels = ['T1-Na', 'T1-La', 'T4-T2', 'T2-credit','T4-T3', 'T3-Em','T4-T2', 'T2-Secode','T4-T2', 'T4-T2', 'T2-Mo','O']

# Generate and save augmented sentences
output_file = 'E_28.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#########################################################################################
#####################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@email.com','credit card', '3530567226316942', 'securitycode', '123', 'owner', 'Emily', 'Williams', 'charge', '$', '150',  '.']
original_labels = ['T4-T3', 'T3-Em','T4-T2', 'T2-credit','T4-T2', 'T2-Secode','T4-T1','T1-Na', 'T1-La','T4-T2', 'T4-T2', 'T2-Mo','O']

# Generate and save augmented sentences
output_file = 'E_29.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#####################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@email.com','credit card', '3530567226316942', 'securitycode', '123', 'owner', 'Emily', 'Williams', 'charge', '$', '150',  '.']
original_labels = ['T4-T3', 'T3-Em','T4-T2', 'T2-credit','T4-T2', 'T2-Secode', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T2', 'T4-T2', 'T2-Mo', 'O']

# Generate and save augmented sentences
output_file = 'E_30.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

###########################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@email.com','credit card', '3530567226316942', 'owner', 'Emily', 'Williams','securitycode', '123','charge', '$', '150',  '.']
original_labels = ['T4-T3', 'T3-Em','T4-T2','T2-credit','T4-T1', 'T1-Na', 'T1-La','T4-T2', 'T2-Secode','T4-T2', 'T4-T2', 'T2-Mo', 'O']

# Generate and save augmented sentences
output_file = 'E_31.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#############################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@email.com','credit card', '3530567226316942', 'owner', 'Emily', 'Williams','securitycode', '123','charge', '$', '150',  '.']
original_labels = ['T4-T3', 'T3-Em','T4-T2', 'T2-credit','T4-T1', 'T1-Na', 'T1-La','T4-T2','T2-Secode','T4-T2', 'T4-T2', 'T2-Mo','O']

# Generate and save augmented sentences
output_file = 'E_32.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#####################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['securitycode', '123','email', 'alex.johnson@email.com','credit card', '3530567226316942', 'owner', 'Emily', 'Williams','charge', '$', '150',  '.']
original_labels = ['T4-T2','T2-Secode','T4-T3', 'T3-Em','T4-T2','T2-credit','T4-T1', 'T1-Na', 'T1-La','T4-T2', 'T4-T2', 'T2-Mo', 'O']

# Generate and save augmented sentences
output_file = 'E_33.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
########################################################################################################33
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['Douglas', 'Matthew', 'SSN', '899-53-7468', 'email', 'alex.johnson@email.com',
                   'credit card', '3530567226316942', 'securitycode', '123', '.']
original_labels = ['T1-Na', 'T1-La', 'T4-T1', 'T1-Ss','T4-T3', 'T3-Em','T4-T2','T2-credit','T4-T2','T2-Secode','O']

# Generate and save 500 augmented sentences
output_file = 'E_34.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['Douglas', 'Matthew','email', 'alex.johnson@email.com','SSN', '899-53-7468',
                   'credit card', '3530567226316942', 'securitycode', '123', '.']
original_labels = ['T1-Na', 'T1-La','T4-T3', 'T3-Em', 'T4-T1','T1-Ss','T4-T2','T2-credit','T4-T2','T2-Secode', 'O']

# Generate and save 500 augmented sentences
output_file = 'E_35.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
####################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['Douglas', 'Matthew','email', 'alex.johnson@email.com','credit card', '3530567226316942','SSN', '899-53-7468',
                   'securitycode', '123', '.']
original_labels = ['T1-Na', 'T1-La','T4-T3', 'T3-Em','T4-T2','T2-credit','T4-T1', 'T1-Ss','T4-T2','T2-Secode','O']

# Generate and save 500 augmented sentences
output_file = 'E_36.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

##################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['Douglas', 'Matthew','credit card', '3530567226316942','email', 'alex.johnson@email.com','SSN', '899-53-7468',
                   'securitycode', '123', '.']
original_labels = ['T1-Na', 'T1-La','T4-T2','T2-credit','T4-T3', 'T3-Em','T4-T1', 'T1-Ss','T4-T2','T2-Secode','O']

# Generate and save 500 augmented sentences
output_file = 'E_37.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##############################################################################################
##################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['Douglas', 'Matthew','SSN', '899-53-7468',
                   'securitycode', '123','email','alex.johnson@email.com','credit card', '3530567226316942','.']
original_labels = ['T1-Na', 'T1-La','T4-T1', 'T1-Ss','T4-T2','T2-Secode','T4-T3','T3-Em','T4-T2','T2-credit','O']

# Generate and save 500 augmented sentences
output_file = 'E_38.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#############################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['email','alex.johnson@email.com','owner','Douglas', 'Matthew','SSN', '899-53-7468',
                   'security code', '123','credit card', '3530567226316942','.']
original_labels = ['T4-T3','T3-Em','T4-T1','T1-Na', 'T1-La','T4-T1', 'T1-Ss','T4-T2','T2-Secode','T4-T2','T2-credit','O']

# Generate and save 500 augmented sentences
output_file = 'E_39.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#######################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@email.com', 'owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468','credit card', '3530567226316942','securitycode', '123', '.']
original_labels = ['T4-T3','T3-Em','T4-T1','T1-Na', 'T1-La','T4-T1', 'T1-Ss','T4-T2','T2-credit','T4-T2','T2-Secode','O']

# Generate and save 500 augmented sentences
output_file = 'E_40.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@email.com', 'owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468', 'securitycode', '123', 'credit card', '3530567226316942', '.']
original_labels = ['T4-T3','T3-Em','T4-T1','T1-Na', 'T1-La','T4-T1','T1-Ss','T4-T2','T2-Secode','T4-T2','T2-credit','O']

# Generate and save 500 augmented sentences
output_file = 'E_41.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@email.com','credit card', '3530567226316942', 'owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468', 'securitycode', '123', '.']
original_labels = ['T4-T3','T3-Em','T4-T2','T2-credit','T4-T1','T1-Na', 'T1-La','T4-T1','T1-Ss','T4-T2','T2-Secode','O']

# Generate and save 500 augmented sentences
output_file = 'E_42.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'email', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@email.com','credit card', '3530567226316942','securitycode', '123', 'owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468', '.']
original_labels = ['T4-T3','T3-Em','T4-T2','T2-credit','T4-T2','T2-Secode','T4-T1','T1-Na', 'T1-La','T4-T1','T1-Ss','O']

# Generate and save 500 augmented sentences
output_file = 'E_43.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#####################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942','email', 'alex.johnson@email.com','securitycode', '123', 'owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468', '.']
original_labels = ['T4-T2','T2-credit','T4-T3','T3-Em','T4-T2','T2-Secode','T4-T1','T1-Na', 'T1-La','T4-T1','T1-Ss','O']

# Generate and save 500 augmented sentences
output_file = 'E_44.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#############################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'email', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942','securitycode', '123','email', 'alex.johnson@email.com', 'owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468', '.']
original_labels = ['T4-T2','T2-credit','T4-T2','T2-Secode','T4-T3','T3-Em','T4-T1','T1-Na', 'T1-La','T4-T1','T1-Ss','O']

# Generate and save 500 augmented sentences
output_file = 'E_45.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#############################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'email', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942','securitycode','123', 'SSN', '899-53-7468','email', 'alex.johnson@email.com', 'owner', 'Douglas', 'Matthew', 
                   '.']
original_labels = ['T4-T2','T2-credit','T4-T2','T2-Secode','T4-T1','T1-Ss','T4-T3','T3-Em','T4-T1','T1-Na', 'T1-La','O']

# Generate and save 500 augmented sentences
output_file = 'E_46.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
####################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942','securitycode','123','email', 'alex.johnson@email.com','SSN', '899-53-7468', 'owner', 'Douglas', 'Matthew', 
                   '.']
original_labels = ['T4-T2','T2-credit','T4-T2','T2-Secode','T4-T3','T3-Em','T4-T1','T1-Ss','T4-T1','T1-Na', 'T1-La','O']

# Generate and save 500 augmented sentences
output_file = 'E_47.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

##########################################################################################   M_STARTES
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']

# Function to augment sentence tokens with SSN, name, IP address, email, and owner synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1', 'email', 'alex.johnson@gmail.com', 'SSN', '123-45-6789', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Ss', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_48.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#############################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']

# Function to augment sentence tokens with SSN, name, IP address, email, and owner synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1','SSN', '123-45-6789','email', 'alex.johnson@gmail.com', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip','T4-T1', 'T1-Ss','T4-T3', 'T3-Em','T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_49.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

########################################################################################################

from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']

# Function to augment sentence tokens with SSN, name, IP address, email, and owner synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1','SSN', '123-45-6789','email', 'alex.johnson@gmail.com', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip','T4-T1', 'T1-Ss','T4-T3', 'T3-Em','T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_50.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

##################################################################################################


from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'email', 'electronicmail']

# Function to augment sentence tokens with SSN, name, IP address, email, and owner synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1','charge', '$', '150','SSN', '123-45-6789','email', 'alex.johnson@gmail.com', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip','T4-T2', 'T4-T2', 'T2-Mo','T4-T1', 'T1-Ss','T4-T3', 'T3-Em','T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_51.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1', 'charge', '$', '150', 'SSN', '123-45-6789', 
                   'email', 'alex.johnson@gmail.com', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Ss',
                   'T4-T3', 'T3-Em', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_52.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##################################################################################### 
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1', 'charge', '$', '150', 'phonenumber', '617 568-9833', 
                   'email', 'alex.johnson@gmail.com', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Pho',
                   'T4-T3', 'T3-Em', 'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_53.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)


###################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1', 'charge', '$', '150','email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip', 'T4-T2', 'T4-T2', 'T2-Mo','T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_54.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

###############################################################################################################

from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'email', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942','securitycode','123', 'owner', 'Douglas', 'Matthew', 
                   '.']
original_labels = ['T4-T2','T2-credit','T4-T2','T2-Secode','T4-T1','T1-Na', 'T1-La','O']

# Generate and save 500 augmented sentences
output_file = 'E_55.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#####################################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['securitycode', '123', 'credit card', '3530567226316942', 'owner', 'Emily', 'Williams','charge', '$', '150',  '.']
original_labels = ['T4-T2','T2-Secode','T4-T2','T2-credit','T4-T1', 'T1-Na', 'T1-La','T4-T2', 'T4-T2', 'T2-Mo', 'O']

# Generate and save augmented sentences
output_file = 'E_56.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##############################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['creditcard', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942', 'owner', 'Emily', 'Williams','securitycode', '123','charge', '$', '150',  '.']
original_labels = ['T4-T2', 'T2-credit','T4-T1', 'T1-Na', 'T1-La','T4-T2','T2-Secode','T4-T2', 'T4-T2', 'T2-Mo','O']

# Generate and save augmented sentences
output_file = 'E_57.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942', 'owner', 'Emily', 'Williams','securitycode', '123',  '.']
original_labels = ['T4-T2', 'T2-credit','T4-T1', 'T1-Na', 'T1-La','T4-T2','T2-Secode','O']

# Generate and save augmented sentences
output_file = 'E_58.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##############################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['owner', 'Emily', 'Williams','charge', '$', '150',  '.']
original_labels = ['T4-T1', 'T1-Na', 'T1-La','T4-T2', 'T4-T2', 'T2-Mo','O']

# Generate and save augmented sentences
output_file = 'E_59.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

###########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost','transaction']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV','CVV2', 'cardverificationcode']  # Synonyms for security code

# Function to generate a unique first name
def get_unique_first_name(used_first_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.first_name()
        if new_name not in used_first_names:
            return new_name
        attempts += 1
    return fake.first_name()  # Fallback to just generating a random name

# Function to generate a unique last name
def get_unique_last_name(used_last_names):
    attempts = 0
    while attempts < 10:  # Limit attempts to find a unique name
        new_name = fake.last_name()
        if new_name not in used_last_names:
            return new_name
        attempts += 1
    return fake.last_name()  # Fallback to just generating a random name

# Function to replace certain tokens with augmented ones using Faker and synonyms
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    
    for i, token in enumerate(tokens):
        # Keep the dollar sign unchanged
        if token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount
        # Replace email and email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with random synonym for 'email'
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # Generate random email
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email
        # Replace owner and synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym for 'owner'
        # Replace charge and synonyms
        elif token in synonyms_for_charge:
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with random synonym for 'charge'
        # Replace credit card and synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))  # Replace with random synonym for 'credit card'
        # Replace security code and synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))  # Replace with random synonym for 'security code'
        # Replace specific first name
        elif token == 'Emily':
            new_first_name = get_unique_first_name(used_first_names)
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        # Replace specific last name
        elif token == 'Williams':
            new_last_name = get_unique_last_name(used_last_names)
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        # Replace credit card number with a generated value
        elif token.isdigit() and len(token) == 16:  # If token is a 16-digit credit card number
            credit_card_number = fake.credit_card_number()  # Generate a random credit card number
            augmented_tokens.append(credit_card_number)  # Replace with generated credit card number
        # Replace security code with a generated value
        elif token.isdigit() and len(token) == 3:  # If token is a 3-digit security code (CVV)
            security_code = fake.credit_card_security_code()  # Generate a random security code
            augmented_tokens.append(security_code)  # Replace with generated security code
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()   # Set to track used last names

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['charge', '$', '150','owner', 'Emily','Williams', '.']
original_labels = ['T4-T2', 'T4-T2', 'T2-Mo','T4-T1', 'T1-Na', 'T1-La','O']

# Generate and save augmented sentences
output_file = 'E_60.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IPaddress', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_birthday = ['birthday', 'born', 'date birth']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names, generated_data):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated
    birthday_generated = False  # Flag to track if birthday has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily' and token not in generated_data["first_names"]:
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            generated_data["first_names"].add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith' and token not in generated_data["last_names"]:
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            generated_data["last_names"].add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "phone number" with synonyms
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Replace with synonym for "phone number"

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Replace "birthday" with synonyms and generate random birthday
        elif token == 'birthday' and not birthday_generated:
            augmented_tokens.append(random.choice(synonyms_for_birthday))  # Replace with birthday synonym
            month = fake.month_name()
            day = str(random.randint(1, 28))  # Assuming up to 28 days to avoid invalid dates
            year = str(random.randint(1980, 2020))
            birthday = f"{month} {day} {year}"
            augmented_tokens.append(birthday)  # Add random birthday
            birthday_generated = True
            i += 4  # Skip the original date tokens
            continue

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()
    generated_data = {"first_names": set(), "last_names": set(), "owners": set()}

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names, generated_data)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['phonenumber', '617 568-9833', 'living', '123', 'Maple', 'St', 'Springfield', 'email', 'alex.johnson@gmail.com', 'birthday', 'March', '15', '1990','owner','Emily','Smith', '.']
original_labels = ['T4-T1', 'T1-Pho', 'T4-T1', 'T1-St', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Bi','T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_61.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#####################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield', 'IP address', '192.168.1.1', 'charge', '$', '150',
                   'email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T1', 'T1-St','T4-T3', 'T3-Ip', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_62.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'email', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield', 'charge', '$', '150','IP address', '192.168.1.1',
                   'email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T1', 'T1-St','T4-T2', 'T4-T2', 'T2-Mo','T4-T3', 'T3-Ip', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_63.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
############################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield', 'charge', '$', '150',
                   'email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T1', 'T1-St','T4-T2', 'T4-T2', 'T2-Mo','T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_64.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
############################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@gmail.com','living', '123', 'Maple', 'St', 'Springfield', 'charge', '$', '150',
                    'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Em','T4-T1', 'T1-St','T4-T2', 'T4-T2', 'T2-Mo', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_65.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

####################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@gmail.com','living', '123', 'Maple', 'St', 'Springfield',
                    'phonenumber', '617 568-9833', '.']
original_labels = ['T4-T3', 'T3-Em','T4-T1', 'T1-St', 'T4-T1', 'T1-Pho', 'O']

# Generate and save augmented sentences
output_file = 'E_66.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield','email', 'alex.johnson@gmail.com',
                    'phonenumber', '617 568-9833', '.']
original_labels = ['T4-T1', 'T1-St','T4-T3', 'T3-Em','T4-T1', 'T1-Pho', 'O']

# Generate and save augmented sentences
output_file = 'E_67.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

###########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['phonenumber', '617 568-9833','living', '123', 'Maple', 'St', 'Springfield','email', 'alex.johnson@gmail.com',
                     '.']
original_labels = ['T4-T1', 'T1-Pho','T4-T1', 'T1-St','T4-T3', 'T3-Em','O']

# Generate and save augmented sentences
output_file = 'E_68.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

###########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['phonenumber','617 568-9833','email', 'alex.johnson@gmail.com', 'living', '123', 'Maple', 'St', 'Springfield',
                     '.']
original_labels = ['T4-T1', 'T1-Pho','T4-T3', 'T3-Em','T4-T1', 'T1-St','O']

# Generate and save augmented sentences
output_file = 'E_69.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV', 'CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))
        # Replace actual bank name (e.g., America) with a single token company name
        elif token == 'America' and i > 0 and tokens[i - 1] == 'bank':
            bank_name = fake.company()  # Fake company name as bank name
            bank_name_tokens = bank_name.split()  # Split into single tokens
            augmented_tokens.append(bank_name_tokens[0])  # Only add the first token of the company name
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942', 'bank', 'America', 'email', 'alex.johnson@email.com', 'securitycode', '123', 'owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468', '.']
original_labels = ['T4-T2', 'T2-credit', 'T4-T2', 'T2-bank', 'T4-T3', 'T3-Em', 'T4-T2', 'T2-Secode', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T1', 'T1-Ss', 'O']

# Generate and save 500 augmented sentences
output_file = 'E_70.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

###################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV', 'CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'BankOfAmerica', 'HSBC']  # List of bank names

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))
        # Replace actual bank name (e.g., America) with a random bank name
        elif token == 'America' and i > 0 and tokens[i - 1] == 'bank':
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['credit card', '3530567226316942', 'bank', 'America', 'email', 'alex.johnson@email.com', 'securitycode', '123', 'owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468', '.']
original_labels = ['T4-T2', 'T2-credit', 'T4-T2', 'T2-bank', 'T4-T3', 'T3-Em', 'T4-T2', 'T2-Secode', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T1', 'T1-Ss', 'O']

# Generate and save 500 augmented sentences
output_file = 'E_71.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

##########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV', 'CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'BankOfAmerica', 'HSBC']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))
        # Replace actual bank names with a random name from the bank_names list
        elif token == 'America' and i > 0 and tokens[i - 1] == 'bank':
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['bank', 'America', 'credit card', '3530567226316942', 'email', 'alex.johnson@email.com', 'securitycode', '123', 'owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468', '.']
original_labels = ['T4-T2', 'T2-bank', 'T4-T2', 'T2-credit', 'T4-T3', 'T3-Em', 'T4-T2', 'T2-Secode', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T1', 'T1-Ss', 'O']

# Generate and save 500 augmented sentences
output_file = 'E_72.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)


###########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV', 'CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'BankOfAmerica', 'HSBC']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        # Replace synonyms for bank name with a single token (company name)
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))
        # Replace actual bank name (e.g., America) with a single token (fake company name)
        elif token == 'America' and i > 0 and tokens[i - 1] == 'bank':
            bank_name = random.choice(bank_names)  # Choose a random bank name from the list
            augmented_tokens.append(bank_name)  # Add the bank name
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@email.com','bank', 'America','credit card', '3530567226316942','securitycode', '123', 'owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468', '.']
original_labels = ['T4-T3', 'T3-Em','T4-T2', 'T2-bank','T4-T2', 'T2-credit','T4-T2', 'T2-Secode', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T1', 'T1-Ss', 'O']

# Generate and save 500 augmented sentences
output_file = 'E_73.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

############################################################################################################
from faker import Faker
import random

# Initialize Faker instance to generate fake data
fake = Faker()

# Synonym lists for different entities that can be augmented
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV', 'CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Function to augment tokens in a sentence based on predefined synonym lists
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []  # List to hold the augmented tokens

    # Iterate through each token in the original sentence
    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value with a randomly generated SSN
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace specific first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                # Ensure the new first name is unique
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                # Ensure the new last name is unique
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses with randomly generated ones
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers with randomly generated ones
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers with randomly generated ones
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        # Replace synonyms for bank name with a randomly chosen bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Use a bank synonym from the list
        # Replace "America" after "bank" with a randomly chosen bank name
        elif token == 'America' and i > 0 and tokens[i - 1] == 'bank':
            bank_name = random.choice(bank_names)  # Choose a random bank name from the list
            augmented_tokens.append(bank_name)  # Add the bank name
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save them to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()  # Set to track used first names
    used_last_names = set()  # Set to track used last names

    with open(output_file, 'w') as f_out:
        # Generate multiple augmented sentences
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write corresponding labels

# Original tokens and labels for augmentation
original_tokens = ['securitycode', '123','bank', 'America','credit card', '3530567226316942','owner', 'Douglas', 'Matthew', 
                   'SSN', '899-53-7468', '.']
original_labels = ['T4-T2', 'T2-Secode','T4-T2', 'T2-bank','T4-T2', 'T2-credit', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T1', 'T1-Ss', 'O']

# Generate and save 500 augmented sentences to a file
output_file = 'E_74.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#######################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV', 'CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace synonyms for SSN
        if token in synonyms_for_ssn:
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            augmented_tokens.append(fake.credit_card_number())
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            augmented_tokens.append(fake.credit_card_security_code())
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))
        # Replace bank names from the manual list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))
        # Replace actual bank name following 'bank'
        elif token == 'America' and i > 0 and tokens[i - 1] == 'bank':
            augmented_tokens.append(fake.company())  # Fake company name as bank name
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['securitycode', '123', 'credit card', '3530567226316942', 'owner', 'Douglas', 'Matthew', 'bank', 'America', 
                   'SSN', '899-53-7468', '.']
original_labels = ['T4-T2', 'T2-Secode', 'T4-T2', 'T2-credit', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T2', 'T2-bank', 'T4-T1', 'T1-Ss', 'O']

# Generate and save 500 augmented sentences
output_file = 'E_75.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#####################################################################################################################

from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['credit card', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV', 'CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token in synonyms_for_ssn:
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace email synonyms
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace credit card synonyms
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace security code synonyms
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace owner synonyms
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        # Replace bank name synonyms
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))
        # Replace actual bank names from the manual list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))
        # Replace specific bank names following 'bank'
        elif token == 'America' and i > 0 and tokens[i - 1] == 'bank':
            augmented_tokens.append(fake.company())  # Fake company name as bank name
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = [
    'securitycode', '123', 'credit card', '3530567226316942', 'owner', 'Douglas', 'Matthew', 
    'SSN', '899-53-7468', 'bank', 'America', '.'
]
original_labels = [
    'T4-T2', 'T2-Secode', 'T4-T2', 'T2-credit', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T1', 'T1-Ss', 
    'T4-T2', 'T2-bank', 'O'
]

# Generate and save 500 augmented sentences
output_file = 'E_76.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
######################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonym lists
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_credit_card = ['creditcard', 'debitcard', 'paymentcard', 'card']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_security_code = ['securitycode', 'CVC', 'CVV', 'CVV2', 'cardverificationcode']
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Function to augment tokens in the sentence
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []

    for i, token in enumerate(tokens):
        # Replace SSN synonyms
        if token == 'SSN':
            augmented_tokens.append(random.choice(synonyms_for_ssn))
        # Replace SSN value
        elif i > 0 and tokens[i - 1] in synonyms_for_ssn:
            augmented_tokens.append(fake.ssn())
        # Replace first and last names
        elif token in ['Douglas', 'Matthew']:
            if token == 'Douglas':  # Replace first name
                new_first_name = fake.first_name()
                while new_first_name in used_first_names:
                    new_first_name = fake.first_name()
                used_first_names.add(new_first_name)
                augmented_tokens.append(new_first_name)
            else:  # Replace last name
                new_last_name = fake.last_name()
                while new_last_name in used_last_names:
                    new_last_name = fake.last_name()
                used_last_names.add(new_last_name)
                augmented_tokens.append(new_last_name)
        # Replace synonyms for email
        elif token in synonyms_for_email:
            augmented_tokens.append(random.choice(synonyms_for_email))
        # Replace email addresses
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)
        # Replace synonyms for credit card
        elif token in synonyms_for_credit_card:
            augmented_tokens.append(random.choice(synonyms_for_credit_card))
        # Replace credit card numbers
        elif token.isdigit() and len(token) == 16:
            credit_card_number = fake.credit_card_number()
            augmented_tokens.append(credit_card_number)
        # Replace synonyms for security code
        elif token in synonyms_for_security_code:
            augmented_tokens.append(random.choice(synonyms_for_security_code))
        # Replace security code numbers
        elif token.isdigit() and len(token) == 3:
            security_code = fake.credit_card_security_code()
            augmented_tokens.append(security_code)
        # Replace synonyms for owner
        elif token in synonyms_for_owner:
            augmented_tokens.append(random.choice(synonyms_for_owner))
        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))
        # Replace bank names using manual list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))
        else:
            augmented_tokens.append(token)  # Keep other tokens unchanged

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")

# Original Tokens and Labels
original_tokens = ['securitycode', '123', 'bank', 'America', 'credit card', '3530567226316942', 'owner', 'Douglas', 'Matthew', 'SSN', '899-53-7468', '.']
original_labels = ['T4-T2', 'T2-Secode', 'T4-T2', 'T2-bank', 'T4-T2', 'T2-credit', 'T4-T1', 'T1-Na', 'T1-La', 'T4-T1', 'T1-Ss', 'O']

# Generate and save 500 augmented sentences
output_file = 'E_77.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1', 'charge', '$', '150','bank', 'America','email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip', 'T4-T2', 'T4-T2', 'T2-Mo','T4-T2', 'T2-bank','T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_78.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#########################################################################################################################
#########################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1', 'charge', '$', '150','bank', 'America','website','aliinstagram.com', 
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip', 'T4-T2', 'T4-T2', 'T2-Mo','T4-T2', 'T2-bank', 'T4-T3', 'T3-web',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_79.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#########################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1', 'charge', '$', '150','website','aliinstagram.com','bank', 'America',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip', 'T4-T2', 'T4-T2', 'T2-Mo','T4-T3', 'T3-web','T4-T2', 'T2-bank', 
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_80.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#########################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1', 'charge', '$', '150','website','aliinstagram.com','bank', 'America', 
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip', 'T4-T2', 'T4-T2', 'T2-Mo','T4-T3', 'T3-web','T4-T2', 'T2-bank', 
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_81.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#############################################################################################################
#########################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1','website','aliinstagram.com', 'charge', '$', '150','bank', 'America',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip','T4-T3','T3-web','T4-T2','T4-T2','T2-Mo','T4-T2','T2-bank', 
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_82.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#############################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1','bank', 'America','email', 'alex.johnson@gmail.com','website','aliinstagram.com','phonenumber', '617 568-9833',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Ip','T4-T2', 'T2-bank','T4-T3', 'T3-Em','T4-T3','T3-web','T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_83.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

###########################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['website','aliinstagram.com','IP address', '192.168.1.1','phonenumber', '617 568-9833','email', 'alex.johnson@gmail.com',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3','T3-web','T4-T3','T3-Ip','T4-T1', 'T1-Pho','T4-T3', 'T3-Em',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_84.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#####################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['website','aliinstagram.com','owner', 'Emily', 'Smith','IP address','192.168.1.1','phonenumber', '617 568-9833','email', 'alex.johnson@gmail.com',
                     '.']
original_labels = ['T4-T3','T3-web','T4-T1', 'T1-Na', 'T1-La','T4-T3','T3-Ip','T4-T1', 'T1-Pho','T4-T3', 'T3-Em',
                    'O']

# Generate and save augmented sentences
output_file = 'E_85.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#############################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['owner', 'Emily', 'Smith','website','aliinstagram.com','IP address','192.168.1.1','phonenumber', '617 568-9833','email', 'alex.johnson@gmail.com',
                     '.']
original_labels = ['T4-T1', 'T1-Na', 'T1-La','T4-T3','T3-web','T4-T3','T3-Ip','T4-T1', 'T1-Pho','T4-T3', 'T3-Em',
                    'O']

# Generate and save augmented sentences
output_file = 'E_86.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#############################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['owner', 'Emily', 'Smith','website','aliinstagram.com','IP address','192.168.1.1','phonenumber', '617 568-9833','email', 'alex.johnson@gmail.com',
                     '.']
original_labels = ['T4-T1', 'T1-Na', 'T1-La','T4-T3','T3-web','T4-T3','T3-Ip','T4-T1', 'T1-Pho','T4-T3', 'T3-Em',
                    'O']

# Generate and save augmented sentences
output_file = 'E_87.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postalcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']  # Added synonyms for country

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['phonenumber','617 568-9833','email', 'alex.johnson@gmail.com','living', '123', 'Maple', 'St', 'Springfield','zipcode','1234','country','US', '.']
original_labels = ['T4-T1', 'T1-Pho','T4-T3', 'T3-Em','T4-T1', 'T1-St','T4-T1', 'T1-Zip','T4-T1', 'T1-Count','O']

# Generate and save augmented sentences
output_file = 'E_88.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#####################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postalcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']  # Added synonyms for country

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['phonenumber','617 568-9833','email', 'alex.johnson@gmail.com','living', '123', 'Maple', 'St', 'Springfield','country','US','zipcode','1234', '.']
original_labels = ['T4-T1', 'T1-Pho','T4-T3', 'T3-Em','T4-T1', 'T1-St','T4-T1', 'T1-Count','T4-T1', 'T1-Zip','O']

# Generate and save augmented sentences
output_file = 'E_89.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

##################################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postalcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']  # Added synonyms for country

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['phonenumber','617 568-9833','zipcode','1234','email', 'alex.johnson@gmail.com','living', '123', 'Maple', 'St', 'Springfield','country','US', '.']
original_labels = ['T4-T1', 'T1-Pho','T4-T1', 'T1-Zip','T4-T3', 'T3-Em','T4-T1', 'T1-St','T4-T1', 'T1-Count','O']

# Generate and save augmented sentences
output_file = 'E_90.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###########################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postalcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"

        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['owner', 'Emily', 'Smith', 'zipcode', '1234', 'website', 'aliinstagram.com', 'IP address',
                   '192.168.1.1', 'phonenumber', '617 568-9833', 'email', 'alex.johnson@gmail.com', 'country', 'US', '.']
original_labels = ['T4-T1', 'T1-Na', 'T1-La','T4-T1', 'T1-Zip','T4-T3', 'T3-web', 'T4-T3', 'T3-Ip', 'T4-T1', 'T1-Pho', 'T4-T3', 'T3-Em','T4-T1', 'T1-Count', 'O']

# Generate and save augmented sentences
output_file = 'E_91.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###############################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postalcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"

        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['owner', 'Emily','Smith','phonenumber', '617 568-9833', 'zipcode', '1234', 'website', 'aliinstagram.com','country', 'US','IP address',
                   '192.168.1.1', 'email', 'alex.johnson@gmail.com', '.']
original_labels = ['T4-T1', 'T1-Na', 'T1-La','T4-T1', 'T1-Pho','T4-T1', 'T1-Zip','T4-T3', 'T3-web','T4-T1', 'T1-Count','T4-T3', 'T3-Ip', 'T4-T3', 'T3-Em','O']

# Generate and save augmented sentences
output_file = 'E_92.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##############################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postalcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"

        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['owner', 'Emily','Smith','website', 'aliinstagram.com','phonenumber', '617 568-9833', 'zipcode', '1234','country', 'US','IP address',
                   '192.168.1.1', 'email', 'alex.johnson@gmail.com', '.']
original_labels = ['T4-T1', 'T1-Na', 'T1-La','T4-T3', 'T3-web','T4-T1', 'T1-Pho','T4-T1', 'T1-Zip','T4-T1', 'T1-Count','T4-T3', 'T3-Ip', 'T4-T3', 'T3-Em','O']

# Generate and save augmented sentences
output_file = 'E_93.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
####################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield', 'IP address', '192.168.1.1', 'charge', '$', '150',
                   'email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', 
                   'zipcode', '1234', 'country', 'US', '.']
original_labels = ['T4-T1', 'T1-St', 'T4-T3', 'T3-Ip', 'T4-T2', 'T4-T2', 'T2-Mo', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La','T4-T1', 'T1-Zip','T4-T1', 'T1-Count', 'O']

# Generate and save augmented sentences
output_file = 'E_94.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#######################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield', 'IP address', '192.168.1.1','zipcode', '1234', 'charge', '$', '150',
                   'email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', 
                    'country', 'US', '.']
original_labels = ['T4-T1', 'T1-St', 'T4-T3', 'T3-Ip','T4-T1', 'T1-Zip','T4-T2', 'T4-T2', 'T2-Mo', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La','T4-T1', 'T1-Count', 'O']

# Generate and save augmented sentences
output_file = 'E_95.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

##############################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield', 'IP address', '192.168.1.1','zipcode', '1234','country', 'US', 'charge', '$', '150',
                   'email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', 
                     '.']
original_labels = ['T4-T1', 'T1-St', 'T4-T3', 'T3-Ip','T4-T1', 'T1-Zip','T4-T1', 'T1-Count','T4-T2', 'T4-T2', 'T2-Mo', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La','O']

# Generate and save augmented sentences
output_file = 'E_96.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###################################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield','zipcode', '1234','IP address', '192.168.1.1','country', 'US', 'charge', '$', '150',
                   'email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', 
                     '.']
original_labels = ['T4-T1', 'T1-St','T4-T1', 'T1-Zip', 'T4-T3', 'T3-Ip','T4-T1', 'T1-Count','T4-T2', 'T4-T2', 'T2-Mo', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La','O']

# Generate and save augmented sentences
output_file = 'E_97.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###########################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield','country', 'US','IP address', '192.168.1.1','zipcode', '1234', 'charge', '$', '150',
                   'email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', 
                     '.']
original_labels = ['T4-T1', 'T1-St','T4-T1', 'T1-Count','T4-T3', 'T3-Ip','T4-T1', 'T1-Zip','T4-T2', 'T4-T2', 'T2-Mo', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La','O']

# Generate and save augmented sentences
output_file = 'E_98.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#####################################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield','country', 'US','charge', '$', '150','zipcode', '1234','IP address', '192.168.1.1',
                   'email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', 
                     '.']
original_labels = ['T4-T1', 'T1-St','T4-T1', 'T1-Count','T4-T2', 'T4-T2', 'T2-Mo','T4-T1', 'T1-Zip','T4-T3', 'T3-Ip', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La','O']

# Generate and save augmented sentences
output_file = 'E_99.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_living = ['living', 'go', 'support', 'populate', 'live', 'know', 'life', 'livelihood', 'be', 'animation', 'keep']
synonyms_for_zip_code = ['zipcode', 'postalcode', 'zip', 'postcode']
synonyms_for_country = ['country', 'nation', 'state', 'land', 'territory']

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle "living" synonyms and street address generation
        if token == 'living' or token in synonyms_for_living:
            augmented_tokens.append(random.choice(synonyms_for_living))  # Replace with a synonym for "living"
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                building_number = fake.building_number()
                street_name = fake.word().capitalize()  # Single word for street name
                city = fake.city().split()[0]  # Single word for city
                street_address = f"{building_number} {street_name} St {city}"
                augmented_tokens.append(street_address)
                i += 4  # Skip the next 4 tokens that make up the full address
            else:
                augmented_tokens.append(token)  # Keep the original token if no address follows
            i += 1
            continue

        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            i += 1
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            i += 1
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name

        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace "zipcode" with synonyms and generate a fake zip code
        elif token in synonyms_for_zip_code:
            augmented_tokens.append(random.choice(synonyms_for_zip_code))  # Add synonym for "zip code"
        elif token == '1234' and i > 0 and tokens[i - 1] in synonyms_for_zip_code:
            augmented_tokens.append(fake.zipcode())  # Generate a random zip code

        # Replace "country" with synonyms and generate a fake country name
        elif token in synonyms_for_country:
            augmented_tokens.append(random.choice(synonyms_for_country))  # Add synonym for "country"
        elif token == 'US' and i > 0 and tokens[i - 1] in synonyms_for_country:
            augmented_tokens.append(fake.country())  # Generate a random country name containing a single word

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

        i += 1

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['living', '123', 'Maple', 'St', 'Springfield','country', 'US','charge', '$', '150','IP address', '192.168.1.1',
                   'email', 'alex.johnson@gmail.com', 'phonenumber', '617 568-9833', 'owner', 'Emily', 'Smith', 'zipcode', '1234',
                     '.']
original_labels = ['T4-T1', 'T1-St','T4-T1', 'T1-Count','T4-T2', 'T4-T2', 'T2-Mo','T4-T3', 'T3-Ip', 'T4-T3', 'T3-Em', 'T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La','T4-T1', 'T1-Zip','O']

# Generate and save augmented sentences
output_file = 'E_100.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

############################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['website','aliinstagram.com','mail','alex.johnson@gmail.com','owner', 'Emily', 'Smith', '.']

original_labels = ['T4-T3','T3-web','T4-T3', 'T3-Em',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_101.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
######################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['website','aliinstagram.com','phonenumber', '617 568-9833',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3','T3-web','T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_102.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
##################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['email', 'alex.johnson@gmail.com','IP address', '192.168.1.1','phonenumber', '617 568-9833',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3', 'T3-Em','T4-T3','T3-Ip','T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_103.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

###############################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['website','aliinstagram.com','phonenumber', '617 568-9833','email', 'alex.johnson@gmail.com',
                     '.']
original_labels = ['T4-T3','T3-web','T4-T1', 'T1-Pho','T4-T3', 'T3-Em',
                    'O']

# Generate and save augmented sentences
output_file = 'E_104.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#########################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['website','aliinstagram.com','email', 'alex.johnson@gmail.com',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3','T3-web','T4-T3', 'T3-Em',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_105.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['phonenumber', '617 568-9833','email', 'alex.johnson@gmail.com',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T1', 'T1-Pho','T4-T3', 'T3-Em',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_106.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
#################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['website','aliinstagram.com',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3','T3-web',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_107.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)

#####################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['phonenumber', '617 568-9833',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T1', 'T1-Pho',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_108.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
############################################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['IP address', '192.168.1.1','phonenumber', '617 568-9833','website','aliinstagram.com','email', 'alex.johnson@gmail.com',
                    'owner', 'Emily', 'Smith', '.']
original_labels = ['T4-T3','T3-Ip','T4-T1', 'T1-Pho','T4-T3','T3-web','T4-T3', 'T3-Em',
                   'T4-T1', 'T1-Na', 'T1-La', 'O']

# Generate and save augmented sentences
output_file = 'E_109.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###############################################################################################################
from faker import Faker
import random

# Initialize Faker instance
fake = Faker()

# Synonyms for various entities
synonyms_for_owner = ['possessor', 'owner', 'proprietor']
synonyms_for_ip = ['IP', 'IP address', 'networkaddress', 'internetprotocol']
synonyms_for_ssn = ['SSN', 'socialsecuritynumber', 'IDnumber']
synonyms_for_email = ['email', 'mail', 'electronicmail']
synonyms_for_charge = ['charge', 'fee', 'expense', 'cost', 'transaction']
synonyms_for_phone_number = ['phonenumber', 'contactnumber', 'mobilenumber', 'telephone']
synonyms_for_bank_name = ['bank', 'financialinstitution', 'lender', 'creditunion', 'bankingservice']
synonyms_for_website = ['website', 'webpage', 'homepage', 'internetpage', 'webportal']

# List of manually created single-word bank names
bank_names = ['Chase', 'WellsFargo', 'Citibank', 'America', 'HSBC']

# Popular website platforms for generating fake websites
popular_platforms = ['twitter', 'instagram', 'facebook', 'youtube', 'amazon']

# Function to generate a fake website based on a platform
def generate_fake_website(platform):
    return f"{fake.user_name()}.{platform}.com"

# Function to augment sentence tokens with various synonyms and random values
def augment_sentence(tokens, used_first_names, used_last_names):
    augmented_tokens = []
    ssn_generated = False  # Flag to track if SSN has been generated

    for i, token in enumerate(tokens):
        # Replace SSN value and use synonyms for "SSN"
        if token == 'SSN' and not ssn_generated and i + 1 < len(tokens):
            augmented_tokens.append(random.choice(synonyms_for_ssn))  # Add synonym for "SSN"
            augmented_tokens.append(fake.ssn())  # Generate a random SSN
            ssn_generated = True  # Set flag to True to prevent further SSN generation
            continue  # Skip to next iteration

        # Skip the original SSN value
        elif token == '123-45-6789' and ssn_generated:
            continue  # Do not add the original SSN value

        # Replace first and last names uniquely
        elif token == 'Emily':
            new_first_name = fake.first_name()
            while new_first_name in used_first_names:
                new_first_name = fake.first_name()
            used_first_names.add(new_first_name)
            augmented_tokens.append(new_first_name)  # Replace with random first name
        elif token == 'Smith':
            new_last_name = fake.last_name()
            while new_last_name in used_last_names:
                new_last_name = fake.last_name()
            used_last_names.add(new_last_name)
            augmented_tokens.append(new_last_name)  # Replace with random last name
        
        # Replace IP address value and use synonyms for "IP address"
        elif token == 'IP address':
            augmented_tokens.append(random.choice(synonyms_for_ip))  # Add synonym for "IP address"
        elif token == '192.168.1.1':
            augmented_tokens.append(fake.ipv4())  # Generate a random IPv4 address

        # Replace email with synonyms or random email addresses
        elif token == 'email':
            augmented_tokens.append(random.choice(synonyms_for_email))  # Replace with email synonym
        elif '@' in token and '.' in token and i > 0 and tokens[i - 1] in synonyms_for_email:
            # 50% chance of generating Gmail or Yahoo; otherwise, a random domain
            if random.choice([True, False]):
                random_email = f"{fake.user_name()}@{random.choice(['gmail.com', 'yahoo.com'])}"
            else:
                random_email = f"{fake.user_name()}@{fake.domain_name()}"
            augmented_tokens.append(random_email)  # Replace with random email

        # Replace "owner" with synonyms
        elif token == 'owner':
            augmented_tokens.append(random.choice(synonyms_for_owner))  # Replace with random synonym

        # Replace "charge" with synonyms
        elif token == 'charge':
            augmented_tokens.append(random.choice(synonyms_for_charge))  # Replace with synonym for "charge"

        # Keep the dollar sign unchanged
        elif token == '$':
            augmented_tokens.append(token)
        # Replace dollar amounts that come after the dollar sign
        elif token.replace(',', '').isdigit() and i > 0 and tokens[i - 1] == '$':
            augmented_tokens.append(str(fake.random_int(min=1, max=10000)))  # Replace with random dollar amount

        # Replace "phone number" with synonyms and generate a fake phone number
        elif token == 'phonenumber':
            augmented_tokens.append(random.choice(synonyms_for_phone_number))  # Add synonym for "phone number"
        elif token == '617 568-9833' and i > 0 and tokens[i - 1] in synonyms_for_phone_number:
            augmented_tokens.append(fake.phone_number())  # Generate a random phone number

        # Replace synonyms for bank name
        elif token in synonyms_for_bank_name:
            augmented_tokens.append(random.choice(synonyms_for_bank_name))  # Add synonym for "bank"
        
        # Replace actual bank name using the manually created list
        elif token in bank_names:
            augmented_tokens.append(random.choice(bank_names))  # Replace with a random bank name from the list

        # Replace "website" and generate a fake website
        elif token == 'website':
            augmented_tokens.append(random.choice(synonyms_for_website))  # Replace with a synonym for "website"
        elif token == 'aliinstagram.com' and i > 0 and tokens[i - 1] in synonyms_for_website:
            augmented_tokens.append(generate_fake_website(random.choice(popular_platforms)))  # Generate a fake website

        # Keep other tokens unchanged
        else:
            augmented_tokens.append(token)

    return augmented_tokens

# Function to generate augmented sentences and save to a file
def generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=5):
    used_first_names = set()
    used_last_names = set()

    with open(output_file, 'w') as f_out:
        for _ in range(num_augments):
            augmented_sentence = augment_sentence(original_tokens, used_first_names, used_last_names)  # Augment the sentence
            f_out.write(f"Augmented Tokens: {augmented_sentence}\n")
            f_out.write(f"Labels: {original_labels}\n\n")  # Write the associated labels

# Original Tokens and Labels
original_tokens = ['phonenumber', '617 568-9833','website','aliinstagram.com','owner', 'Emily', 'Smith','email', 'alex.johnson@gmail.com',
                     '.']
original_labels = ['T4-T1', 'T1-Pho','T4-T3','T3-web','T4-T1', 'T1-Na', 'T1-La','T4-T3', 'T3-Em',
                    'O']

# Generate and save augmented sentences
output_file = 'E_110.txt'
generate_augmented_sentences(output_file, original_tokens, original_labels, num_augments=500)
###########################################################################################################################
import os

# Define the output file name
output_file = 'AUG_all_data4.txt'

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    # Loop through filenames in the desired order from A_1 to A_38
    for i in range(1, 111):
        filename = f"E_{i}.txt"
        # Check if the file exists before trying to open it
        if os.path.isfile(filename):
            with open(filename, 'r') as infile:
                # Read the content of each file and write it to the output file
                outfile.write(infile.read() + "\n")  # Add a newline between files for clarity

print(f"All data from E_1 to E_100 has been combined into {output_file}")

#######################################################################################
# Define the file paths
input_file = "AUG_all_data4.txt"
output_file = "A_Format_AUG4.txt"

# Initialize variables
sentences = []
tokens_list = []
labels_list = []

# Read the input file and extract tokens and labels
with open(input_file, 'r') as file:
    current_tokens = []
    current_labels = []
    
    for line in file:
        line = line.strip()
        
        # Check if the line contains Augmented Tokens
        if line.startswith("Augmented Tokens:"):
            # Extract the tokens
            tokens_str = line.split(": ")[1]
            current_tokens = eval(tokens_str)
        
        # Check if the line contains Labels
        elif line.startswith("Labels:"):
            # Extract the labels
            labels_str = line.split(": ")[1]
            current_labels = eval(labels_str)
            
            # Append the tokens and labels to the lists
            tokens_list.append(current_tokens)
            labels_list.append(current_labels)

# Write to the output file in the required format
with open(output_file, 'w') as file:
    for i, (tokens, labels) in enumerate(zip(tokens_list, labels_list)):
        file.write(f"Sentence {i + 1}:\n")
        file.write(f"Tokens: {tokens}\n")
        file.write(f"Labels: {labels}\n")
        file.write("\n")
        
print(f"Formatted data has been written to {output_file}")

##############################################################################################################
import os

# Define the output file name
output_file = 'AUG_all_data4.txt'

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    # Loop through filenames in the desired order from A_1 to A_38
    for i in range(1, 111):
        filename = f"E_{i}.txt"
        # Check if the file exists before trying to open it
        if os.path.isfile(filename):
            with open(filename, 'r') as infile:
                # Read the content of each file and write it to the output file
                outfile.write(infile.read() + "\n")  # Add a newline between files for clarity

print(f"All data from E_1 to E_100 has been combined into {output_file}")

#######################################################################################
# Define the file paths
input_file = "AUG_all_data4.txt"
output_file = "A_Format_AUG4.txt"

# Initialize variables
sentences = []
tokens_list = []
labels_list = []

# Read the input file and extract tokens and labels
with open(input_file, 'r') as file:
    current_tokens = []
    current_labels = []
    
    for line in file:
        line = line.strip()
        
        # Check if the line contains Augmented Tokens
        if line.startswith("Augmented Tokens:"):
            # Extract the tokens
            tokens_str = line.split(": ")[1]
            current_tokens = eval(tokens_str)
        
        # Check if the line contains Labels
        elif line.startswith("Labels:"):
            # Extract the labels
            labels_str = line.split(": ")[1]
            current_labels = eval(labels_str)
            
            # Append the tokens and labels to the lists
            tokens_list.append(current_tokens)
            labels_list.append(current_labels)

# Write to the output file in the required format
with open(output_file, 'w') as file:
    for i, (tokens, labels) in enumerate(zip(tokens_list, labels_list)):
        file.write(f"Sentence {i + 1}:\n")
        file.write(f"Tokens: {tokens}\n")
        file.write(f"Labels: {labels}\n")
        file.write("\n")
        
print(f"Formatted data has been written to {output_file}")






