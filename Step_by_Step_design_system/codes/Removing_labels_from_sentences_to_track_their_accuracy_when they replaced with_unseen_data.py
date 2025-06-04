# Define the input and output file names
input_filename = '110_aumented_structures.txt'
output_filename = 'structure_augmented_without_label.txt'

# Open the input file for reading and the output file for writing
with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
    # Read all lines in the input file
    lines = infile.readlines()
    
    # Loop through each line and write to the output file if it's not a Labels line
    for line in lines:
        # If the line contains 'Labels:', skip it
        if 'Labels:' not in line:
            outfile.write(line)

print(f"Updated file saved as {output_filename}")
