# Generate mitochondrial benchmark set 
## Introduction
This repository contains a set of scripts and example commands to generate a chrM benchmark set from pangenome-graph-based vcf.

## File Structure
```markdown
└── chrMBenchmarkSet/
    └── 1_create_chrm_benchmarkset.py
```

## Software requirement
* Python 3
* Biopython


## Step 1: Generate mitochondrial benchmark set
1) INPUT: output file from Graph-Based-Benchmark/graphToBenchmarkSet/benchmarkSetGeneration/1_combine_haplotypes.py
2) Reformat headers and append a calculated VAF field (labeled HL).

```jsx
python3 create_chrm_benchmarkset.py -i 9188e8_MSDeComp_comb.vcf -o SMHTHAPMAP6_GRCh38_v1.1.0_somatic_benchmark
```

    
