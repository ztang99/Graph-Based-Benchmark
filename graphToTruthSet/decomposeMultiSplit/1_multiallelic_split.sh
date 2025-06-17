#!/bin/bash

#################################################################
# Step 1: Perform a Multiallelic split on the graph twice
# So graph gaps can be differentieted from multiallelic sites

## author: Andrew Ruttenberg
## contact: ruttenberg.andrew@wustl.edu
#################################################################

numArgs=$#

if [ "$numArgs" -ne 2 ]; then
    echo "Usage: $0 <graph.vcf> <working dir>"
    exit 1
fi


graph=$1
outdir=$2/Step1MultiAllelicSplit
mkdir $outdir

# Run a mutlialleic split twice, labeling splits as . and 0 so if across the two vcfs the genotype are both '.' it's from a grap in the graph
# And if one is '.' and one is '0' its cause the multiallelic split
bcftools norm -m - --multi-overlaps . $graph -Ov -o $outdir/graph.split.dot.vcf
bcftools norm -m - --multi-overlaps 0 $graph -Ov -o $outdir/graph.split.zero.vcf