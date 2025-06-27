# Graph-Based-TruthSet

## Introduction

This repository holds scripts used to generate a pangenome-graph-based variant truth set. 
This truth set generation method successfully generated a highly accurate variant truth set for artificial somatic variants in the HapMap mixture. More information about HapMap cell line mixture can be found here (add link to paper later).

Analyses and validation code mentioned in the manuscript above are in a separate GitHub repository: https://github.com/jinlab-washu/HapMap-TruthSet-Manuscript.git.

## Table of Contents
- [Introduction](#introduction)
- [File structure](#file-structure)
- [Set up for running the pipeline - clone repo](#getting-started)
- [Step 1: generate pangenome graph](#step-1-generate-pangenome-graph)
- [Step 2: generate graph-based truth set](#step-2-generate-variant-truth-set)
    - [Step 2.1: decompose and multi-allelic split](#decomposition-and-multi-allelic-sites-split)
    - [Step 2.2: filter for truth set variants](#truth-set-generation)
- [Cite our work](#citation)

## File Structure
```markdown
├── graphToTruthSet/
    ├── decomposeMultiSplit/
    └── truthSetGeneration/
└── meiTruthSet/
```

## Getting Started
```bash
git clone https://github.com/ztang99/Graph-Based-TruthSet.git
```

## Step 1: Generate Pangenome Graph
Pangenome graphs were built with minigraph-cactus (MC) method following the pipeline described [here](https://github.com/twlab/cig-pipelines/blob/main/wdl/pipelines/pangenome/mcgb.doc.md). More information about minigraph-cactus method can be found [in this paper](https://www.nature.com/articles/s41587-023-01793-w).

This step takes in individual haplotype assemblies, together with a reference genome, to create a pangenome MC graph that captures all variant types (SNVs, indels, and SVs). 

We proceed with the deconstructed VCF file from this pipeline.

## Step 2: Generate Variant Truth Set

All code describing how truth set is generated from pangenome MC graph output VCF is under `graphToTruthSet` subdirectory.

Detailed explanation about how to run each step in truth set generation can be found [here](./graphToTruthSet/README.md).

## Step 3: Generate MEI Truth Set

A detailed illustration of code and example commands used for generating the mobile element insertions (MEI) truth set can be found [here](./meiTruthSet/README.md).

The MEI truth set is based on the structural variant truth set generated in **Step 2**.

## Citation

If you use the graph-based truth set generation pipeline in your work, please consider to cite:

> Add citation later.

