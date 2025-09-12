#!/bin/bash

#################################################################
# Step 3: run RTGtools vcfdecompose to break up MNVs (a common result of the graph building process)
# into the SNVs and Indels that make it up

## author: Andrew Ruttenberg
## contact: ruttenberg.andrew@wustl.edu
#################################################################

numArgs=$#

if [ "$numArgs" -ne 2 ]; then
    echo "Usage: $0 <indir> <outdir>"
    exit 1
fi

inDir=$1
outDir=$2/Step3RTGDecompose
mkdir -p $outDir/dot
mkdir -p $outDir/zero

echo "starting dot graph"
for file in "$inDir"/dot/HG*; do
    nameExt=${file##*/}
    name=${nameExt%.*}
    echo $name
    rtg vcfdecompose --break-indels --break-mnps -i $file -o $outDir/dot/${name}_RTG_Decompose.vcf
    zcat $outDir/dot/${name}_RTG_Decompose.vcf.gz | grep -v "#" > $outDir/dot/${name}_RTG_Decompose.txt
done

echo "starting zero graph"
for file in "$inDir"/zero/HG*; do
    nameExt=${file##*/}
    name=${nameExt%.*}
    echo $name
    rtg vcfdecompose --break-indels --break-mnps -i $file -o $outDir/zero/${name}_RTG_Decompose.vcf
    zcat $outDir/zero/${name}_RTG_Decompose.vcf.gz | grep -v "#" > $outDir/zero/${name}_RTG_Decompose.txt
done