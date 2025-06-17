#!/bin/bash

#################################################################
# Takes in a graph and runs a multiallelic split and decomposition of the MNVs
## author: Andrew Ruttenberg
## contact: ruttenberg.andrew@wustl.edu
#################################################################

numArgs=$#

if [ "$numArgs" -ne 2 ]; then
    echo "Usage: $0 <graph.vcf> <output dir>"
    exit 1
fi

#step 1: multiallelic split

graph=$1
outdir=$2/Step1MultiAllelicSplit
mkdir -p $outdir

cat $graph | grep "#" > $2/header.txt

bcftools norm -m - --multi-overlaps . $graph -Ov -o $outdir/graph.split.dot.vcf
bcftools norm -m - --multi-overlaps 0 $graph -Ov -o $outdir/graph.split.zero.vcf

#step 2, split vcf by haplotype

dotGraph=$outdir/graph.split.dot.vcf
zeroGraph=$outdir/graph.split.zero.vcf
outdir=$2/Step2SplitGraph
mkdir -p $outdir/dot
mkdir -p $outdir/zero

# Seperate the gragh into 12 different VCFs, one for each haplotype
# And do it for both the dot and zero vcf
python3.8 /storage1/fs1/jin810/Active/testing/Ruttenberg/Code/FinalSMAHTCode/MakeGraph/2_split_graph.py -v $dotGraph -o $outdir/dot
python3.8 /storage1/fs1/jin810/Active/testing/Ruttenberg/Code/FinalSMAHTCode/MakeGraph/2_split_graph.py -v $zeroGraph -o $outdir/zero


#step 3: Variant decomposition

inDir=$2/Step2SplitGraph
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

# Step 4: Combine Haplotypes

dot=$2/Step3RTGDecompose/dot
zero=$2/Step3RTGDecompose/zero
outDir=$2/Step4CombineAndSort
mkdir -p $outDir

/usr/bin/python3.8 /storage1/fs1/jin810/Active/testing/Ruttenberg/Code/FinalSMAHTCode/MakeGraph/4_combine_and_sort.py -i $dot -o $outDir/combined_dot.vcf
/usr/bin/python3.8 /storage1/fs1/jin810/Active/testing/Ruttenberg/Code/FinalSMAHTCode/MakeGraph/4_combine_and_sort.py -i $zero -o $outDir/combined_zero.vcf

#Step 5: Merge dot and zero vcfs

dot=$2/Step4CombineAndSort/combined_dot.vcf
zero=$2/Step4CombineAndSort/combined_zero.vcf
header=$2/header.txt
dir=$2/Step5CombineDotAndZero
mkdir -p $dir

/usr/bin/python3.8 /storage1/fs1/jin810/Active/testing/Ruttenberg/Code/FinalSMAHTCode/MakeGraph/5_combine_dot_and_zero.py -z $zero -d $dot -t $header -o $dir/graph.split.and.decompose.vcf