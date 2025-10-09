#################################################################
## 1_modify_vcf_id.py
##
## Add VCF ID for repearmasker run
##
## author: Nahyun Kong 
## contact: nahyun@wustl.edu
#################################################################
import sys
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

# Check if the input file is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <input_vcf_file>")
    sys.exit(1)

# Get the input VCF file from the command line
vcf_file = sys.argv[1]

# List to store the converted FASTA records
fasta_records = []

# Open and read the VCF file
with open(vcf_file, 'r') as vcf:
    for line in vcf:
        # Skip comment lines
        if line.startswith('#'):
            continue
        
        # Split each line
        columns = line.strip().split('\t')
        chrom, pos, id, ref, alt, info = columns[0], columns[1], columns[2], columns[3], columns[4], columns[7]
        
        # Check if the record is an insertion (ALT longer than REF)
        if len(alt) > len(ref):
            # Create a unique index
            unique_index = "{}_{}_{}_{}".format(chrom, pos, id, ref)
            
            # Create a FASTA record
            seq = Seq(alt)
            record = SeqRecord(seq, id=unique_index, description="")
            fasta_records.append(record)

# Write the FASTA records to a file without line wrapping
output_fasta = 'output_insertion.fasta'
with open(output_fasta, 'w') as output_handle:
    SeqIO.write(fasta_records, output_fasta, 'fasta')

# Print the number of sequences in the output
num_sequences = len(fasta_records)
print("VCF file has been successfully converted to FASTA file containing only insertions and saved as {}".format(output_fasta))
print("Number of sequences in the output: {}".format(num_sequences))
