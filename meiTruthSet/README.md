# Generate MEI truth set 
## Introduction
This repository contains a set of scripts and example commands to generate a mobile element insertions(MEI) truth set from pangenome-graph-based SV truth set. The pipeline includes:

* Reassigning unique IDs to VCF records
* Extracting insertion sequences from VCF files
* Annotating sequences using RepeatMasker
* Filtering for young L1 and Alu insertions
* Clipping MEI-related sequence information
  
More information can be found here (add link to paper later).

## File Structure
```markdown
└── meiTruthSet/
    ├── 1_modify_vcf_id.py
    ├── 2_create_fasta.py
    ├── 3_repeatmasker.sh
    └── 4_filter_class_label.py 
```

## Software requirement
* Python 3
* Biopython
* RepeatMasker v4.1.7
  
An existing docker environment with the above packages: veupathdb/repeatmasker:latest

## Step 1: Reassign Unique IDs in VCF
Assigns sequential numeric IDs to VCF entries.

```jsx
python3 1_modify_vcf_id.py input.vcf output.vcf
```

    

## Step 2:  Extract inserted ALT Sequences to FASTA

Extracts all insertion sequences (ALT > REF) from a VCF and outputs to a FASTA file.

```
python3 2_create_fasta.py input.vcf
```
Output: output_insertion.fasta


## Step 3: Annotate Insertion Sequences with RepeatMasker

RepeatMasker must be run with the appropriate database (Dfam) and human species model.
Search Engine: NCBI/RMBLAST [ 2.14.1+ ], Dfam (3.8)

```
RepeatMasker/RepeatMasker -species human -dir {dir} -a output_insertion.fasta

```


## Step 4: Select and Filter for Young MEIs
Filters RepeatMasker-annotated insertions for specific MEI families (L1, Alu) and outputs updated VCF files.

```
# For GRCh38 - L1
python3 4_filter_class_label.py output_insertion.fasta.out input.vcf output_l1.out output_l1.vcf l1

# For GRCh38 - Alu
python3 4_filter_class_label.py output_insertion.fasta.out input.vcf output_alu.out output_alu.vcf alu

# For CHM13 - L1
python3 4_filter_class_label.py output_insertion.fasta.out input.vcf output_l1.out output_l1.vcf l1

# For CHM13 - Alu
python3 4_filter_class_label.py output_insertion.fasta.out input.vcf output_alu.out output_alu.vcf alu

```
* output_insertion.fasta: FASTA with insertion sequences
* *.fasta.out: RepeatMasker annotation
* output_*_mei_*.vcf: Filtered MEI VCFs (L1 or Alu)
