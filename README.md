# Graph-Based-Benchmark

## Introduction

This repository holds scripts used to generate a [pangenome-graph-based variant benchmarking set](https://wangcluster.wustl.edu/~juanfmacias/Graph_based_HapMap_Truth_Set/).
This benchmarking set generation method successfully generated a highly accurate variant benchmarking set for artificial somatic variants in the HapMap mixture. More information about the methodology can be found [here]().

Analyses and validation code mentioned in the manuscript above are in a separate GitHub repository: https://github.com/jinlab-washu/HapMap-BenchmarkSet-Manuscript.git.

## Table of Contents
- [Introduction](#introduction)
- [File structure](#file-structure)
- [Set up for running the pipeline - clone repo](#getting-started)
- [Step 1: generate pangenome graph](#step-1-generate-pangenome-graph)
- [Step 2: generate graph-based benchmarking set](#step-2-generate-variant-benchmarking-set)
- [Step 3: generate MEI benchmarking set](#step-3-generate-mei-benchmarking-set)
- [Cite our work](#citation)

## File Structure
```markdown
├── graphToBenchmarkSet/
    ├── decomposeMultiSplit/
    └── benchmarkSetGeneration/
└── meiBenchmarkSet/
```

## Getting Started
```bash
git clone https://github.com/ztang99/Graph-Based-Benchmark.git
```

## Step 1: Generate Pangenome Graph
Pangenome graphs were built with minigraph-cactus (MC) method following the pipeline described [here](https://github.com/twlab/cig-pipelines/blob/main/wdl/pipelines/pangenome/mcgb.doc.md). More information about minigraph-cactus method can be found [in this paper](https://www.nature.com/articles/s41587-023-01793-w).

This step takes in individual haplotype assemblies, together with a reference genome, to create a pangenome MC graph that captures all variant types (SNVs, indels, and SVs). 

We proceed with the deconstructed VCF file from this pipeline.

## Step 2: Generate Variant benchmarking set

All code describing how benchmarking set is generated from pangenome MC graph output VCF is under `graphToBenchmarkSet` subdirectory.

Detailed explanation about how to run each step in benchmarking set generation can be found [here](./graphToBenchmarkSet/README.md).

## Step 3: Generate MEI benchmarking set

A detailed illustration of code and example commands used for generating the mobile element insertions (MEI) benchmarking set can be found [here](./meiBenchmarkSet/README.md).

The MEI benchmarking set is based on the structural variant benchmarking set generated in **Step 2**.

## Citation

If you use the graph-based benchmarking set generation pipeline in your work, please consider to cite:

> Add citation later.

