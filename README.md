# Graph-Based-TruthSet

## Introduction

This repository holds scripts used to generate a pangenome-graph-based variant truth set. 
This truth set generation method successfully generated a highly accurate variant truth set for artificial somatic variants in the HapMap mixture. More information about HapMap cell line mixture can be found here (add link to paper later).

## File Structure
```markdown
├──graphToTruthSet/
    ├──[decomposition&multi-split]
    └── truthSetGeneration/
└──meiTruthSet/
    └──[extra steps for MEI truth set]
```

## Getting Started
```bash
git clone https://github.com/ztang99/Graph-Based-TruthSet.git
```

## Step 1: Generate Pangenome Graph
Pangenome graphs were built with minigraph-cactus (MC) method following the pipeline described [here](https://github.com/twlab/cig-pipelines/blob/main/wdl/pipelines/pangenome/mcgb.doc.md). More information about minigraph-cactus method can be found [in this paper](https://www.nature.com/articles/s41587-023-01793-w).

This step takes in individual haplotype assemblies, together with a reference genome, to create a pangenome MC graph that captures all variant types (SNVs, indels, and SVs). 

We proceed with the deconstructed VCF file from this pipeline.

## Step 2: Generate Variant Truth set

### Decomposition and multi-allelic sites split
During the pangenome graph construction process, SVs were captured first, and thus all SNVs and indels within the SV will be "nested". The first main step of graph-based truth set generation is to decompose nested variants and split multi-allelic variants harboring the same locus. 

### Truth set generation

#### Prepare Environment
The following software packages are needed to run the code:
```markdown
python3.6 or higher
bgzip
tabix
```
An existing docker environment with the above packages: `elle72/basic:vszt`

#### Run
To run all steps of the following truth set generation code, simply do:
```bash
cd ../Graph-Based_TruthSet/graphToTruthSet/truthSetGeneration
bash 00_run_all.sh $ref_ver $input_vcf $work_dir
```
where `$ref_ver` is the reference used for graph construction (this variable is only used to create sub-directories under output folder for each reference coordinates), `$input_vcf` is the full path to the deconstructed VCF file from **Step 1**, and `$work_dir` denotes the working directory where all results will be written in.

Detailed explanation of each sub-step in truth set generation can be found in `/graphtoTruthSet/README.md`.

## Citation

If you use the graph-based truth set generation pipeline in your work, please consider to cite:

> Add citation later.

Analyses and validation code mentioned in the manuscript above are in a separate GitHub repository: https://github.com/jinlab-washu/HapMap-TruthSet-Manuscript.git.