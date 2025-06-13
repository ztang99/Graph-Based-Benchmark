#!/bin/bash

#################################################################
# This shell script compiles all necessary steps 
# for truth set generation.

## author: Zitian Tang
## contact: tang.zitian@wustl.edu
#################################################################

reff="$1"
input_vcf="$2"
workdir="$3"

if [ "$reff" != "hg38" ] && [ "$reff" != "chm13" ]; then
    echo "Error: reff must be either 'hg38' or 'chm13'"
    exit 1
fi

set -e
mkdir -p "${workdir}/${reff}"
cd "${codedir}" || exit 1

echo "Starting variant processing pipeline..."
echo "Working directory: $workdir"
echo "Input VCF: $input_vcf"

python3 1_combine_haplotypes.py --refver $reff --workdir $workdir --input-file $input_vcf
echo "Step 1 combine haplotypes done!"

python3 2_split_by_var_type.py --refver $reff --workdir $workdir
echo "Step 2 split by variant type done!"

bash 3_reliable_regions.sh $reff $workdir
echo "Step 3 filter for reliable regions done!"

python3 4_reformat_vcf.py --refver $reff --workdir $workdir
echo "Step 4 reformat VCF done!"

python3 5_filter_genotype.py --refver $reff --workdir $workdir
echo "Step 5 filter for somatic variants done!"

bash 6_final_vcf.sh $reff $workdir
echo "Step 6 generate final VCF file done!"


