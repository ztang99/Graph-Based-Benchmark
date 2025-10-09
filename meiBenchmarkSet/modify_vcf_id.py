#################################################################
## 1_modify_vcf_id.py
##
## Add VCF ID for repearmasker run
##
## author: Nahyun Kong 
## contact: nahyun@wustl.edu
#################################################################
import sys

# Check if the input file is provided
if len(sys.argv) < 3:
    print("Usage: python script.py <input_vcf_file> <output_vcf_file>")
    sys.exit(1)

# Get the input and output VCF file from the command line
input_vcf_file = sys.argv[1]
output_vcf_file = sys.argv[2]

# Initialize a counter for the unique ID
unique_id_counter = 1

# Open the input VCF file for reading
with open(input_vcf_file, 'r') as infile, open(output_vcf_file, 'w') as outfile:
    for line in infile:
        # Write header lines unchanged
        if line.startswith('#'):
            outfile.write(line)
            continue
        
        # Split each line into columns
        columns = line.strip().split('\t')
        
        # Assign a sequential unique ID for the ID column
        columns[2] = str(unique_id_counter)
        unique_id_counter += 1
        
        # Write the modified line to the output file
        outfile.write('\t'.join(columns) + '\n')

print(f"VCF file has been successfully modified and saved as {output_vcf_file}")
