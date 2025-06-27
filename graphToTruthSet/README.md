# graphToTruthSet

Code under this directory describes how truth set is generated from pangenome MC graph output VCF.

## File Structure
```markdown
├──decomposeMultiSplit/
    ├── 0_split_and_decompose.sh
    ├── 1_multiallelic_split.sh
    ├── 2_split_graph.py
    ├── 3_rtg_decompose.sh
    ├── 4_combine_and_sort.py
    ├── 5_combine_dot_and_zero.py
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
RTGtools
bcftools 1.22 or higher
```
An existing docker environment with the above packages: `jinlab/pipeline_tools:vs2`

## Run

### decomposeMultiSplit

This directory holds code for variant decomposition and split multi-allelic sites. 

To decompose the variants and split all multi-allelic sites, simply run:
```bash
bash ./decomposeMultiSplit/0_split_and_decompose.sh $graph_vcf $output_dir
```

For more details please see `/decomposeMultiSplit/README.md`.

### truthSetGeneration

This directory holds code to generate the graph-based truth set after variants have been properly decomposed and all multi-allelic sites were split. 

To generate the somatic variant truth set after decomposition and multi-split, simply run:
```bash
bash ./truthSetGeneration/00_run_all.sh $ref_ver $input_vcf $work_dir
```

For more details please see `/truthSetGeneration/README.md`.
