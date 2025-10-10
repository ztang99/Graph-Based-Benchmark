# Generate mitochondrial benchmark set 
## Introduction
This repository contains a set of scripts and example commands to generate a chrM benchmark set from pangenome-graph-based vcf.

## File Structure
```markdown
└── meiBenchmarkSet/
    └── 1_create_chrm_benchmarkset.py
```

## Software requirement
* Python 3
* Biopython


## Step 1: Generate mitochondrial benchmark set
1) Split a combined VCF into SNV, indel, merged small (SNV+indel), and SV VCFs.
2) Reformat headers and append a calculated VAF field (labeled HL).

```jsx
python3 create_chrm_benchmarkset.py -i /storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/zt_temp/mtDNA_true_set_20250507/mtVar_MSDeComp_comb.vcf -o mtVar_MSDeComp_comb
```

    
