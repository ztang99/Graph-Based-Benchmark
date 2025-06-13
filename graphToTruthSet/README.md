# graphToTruthSet

Code under this directory describes how truth set is generated from pangenome MC graph output VCF.

## File Structure
```markdown
├──decomposeMultiSplit/
    └── [code]
└── truthSetGeneration/
    ├── 00_run_all.sh
    ├── 1_combine_haplotypes.py
    ├── 2_split_by_var_type.py
    ├── 3_reliable_regions.sh
    ├── 4_reformat_vcf.py
    ├── 5_filter_genotype.py
    └── 6_final_vcf.sh
```
## Prepare Environment
The following software packages are needed to run the code:
```markdown
python3.6 or higher
bgzip
tabix
```
An existing docker environment with the above packages: `elle72/basic:vszt`

## File Description and Run

Make sure to be in the correct code directory:
```bash
cd ../Graph-Based_TruthSet/graphToTruthSet/truthSetGeneration
```
### 00_run_all.sh
This shell script compiles all necessary code in order.\
To run the entire truth set generation pipeline:
```bash
bash 00_run_all.sh $ref_ver $input_vcf $work_dir
```

### 1_combine_haplotypes.py
A Python script that combines maternal and paternal haplotypes for each variant in the VCF file.

To run this step only:
```bash
python3 1_combine_haplotypes.py --refver $ref_ver --workdir $work_dir --input-file $input_vcf
```

### 2_split_by_var_type.py
A Python script that separates SNVs, indels, and SVs in the in the combined VCF.

To run this step only:
```bash
python3 2_split_by_var_type.py --refver $ref_ver --workdir $work_dir
```

### 3_reliable_regions.sh

A shell script that selects variants within assemblies reliable regions as defined by HPRC.

To run this step only:
```bash
bash 3_reliable_regions.sh $ref_ver $work_dir
```

### 4_reformat_vcf.py

A python script that reformats the VCF headers.

To run this step only:
```bash
python3 4_reformat_vcf.py --refver $ref_ver --workdir $work_dir
```

### 5_filter_genotype.py

A python script that filter genotypes to include only variants that are
homozygous ref in HG005 and have at least one alt in others.

To run this step only:
```bash
python3 5_filter_genotype.py --refver $ref_ver --workdir $work_dir
```

### 6_final_vcf.sh
A bash script that compresses and indexes multiple VCF files under the current directory.

To run this step only:
```bash
bash 6_final_vcf.sh $ref_ver $work_dir
```
