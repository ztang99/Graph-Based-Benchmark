#!/bin/bash

#################################################################
# Step 3: select variants within assemblies reliable regions
# as defined by HPRC.

## author: Nahyun Kong & Zitian Tang.
## contact: nahyun@wustl.edu & tang.zitian@wustl.edu
#################################################################

if [ $# -ne 2 ]; then
    echo "Usage: $0 <refver>"
    echo "refver must be either 'hg38' or 'chm13'"
    exit 1
fi

refver="$1"
workdir="$2"

# Validate refver input
if [ "$refver" != "hg38" ] && [ "$refver" != "chm13" ]; then
    echo "Error: refver must be either 'hg38' or 'chm13'"
    exit 1
fi

# Set reference and reliable_bed based on refver
if [ "$refver" = "hg38" ]; then
    ref="/storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/final_submission/data/reference/hg38/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa"
    # reliable_bed="/storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/output/SMHTHAPMAP6_GRCh38_v1.4_somatic_benchmark.bed"
    reliable_bed="/storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/output/SMHTHAPMAP6_GRCh38_v1.6_somatic_benchmark.bed"
else
    ref="/storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/final_submission/data/reference/chm13/GCA_009914755.4.chrNames.fa"
    # reliable_bed="/storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/output/SMHTHAPMAP6_CHM13_v1.4_somatic_benchmark.bed"
    reliable_bed="/storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/output/SMHTHAPMAP6_CHM13_v1.6_somatic_benchmark.bed"
fi

working_dir="${workdir}/${refver}"
sample_name='9188e8'
echo "Using $refver"
echo "Using reliable bed: $reliable_bed"
cd $working_dir || exit 1

### SNVs ###

snv_file_prefix="${sample_name}_comb_multiSplit_nonorm_dotver_VAFedited_snvs"
## v1.4.2 0228
snv_file_prefix="${sample_name}_MSDeComp_comb_snvs"

( grep '^#' "${snv_file_prefix}.vcf"; bedtools intersect -a "${snv_file_prefix}.vcf" -b $reliable_bed -wa ) > "${snv_file_prefix}_reliable.vcf"

echo "SNV finished!"

### Indels ###

indel_file_prefix="${sample_name}_comb_multiSplit_nonorm_dotver_VAFedited_indels"
## v1.4.2 0228
# indel_file_prefix="${sample_name}_MSDeComp_comb_indels"

## v1.5.2(3?) do bedtools intersect directly
grep '^#' "${indel_file_prefix}.vcf" > "${indel_file_prefix}_reliable.vcf"; bedtools intersect -a "${indel_file_prefix}.vcf" -b $reliable_bed -wa -f 1.0 >> "${indel_file_prefix}_reliable.vcf"

echo "Indel finished!"

### SVs ###

sv_file_prefix="${sample_name}_comb_multiSplit_nonorm_dotver_VAFedited_svs"
## v1.4.2 0228
# sv_file_prefix="${sample_name}_MSDeComp_comb_svs"

## v1.5.2(3?) do bedtools intersect directly
grep '^#' "${sv_file_prefix}.vcf" > "${sv_file_prefix}_reliable.vcf"; bedtools intersect -a "${sv_file_prefix}.vcf" -b $reliable_bed -wa -f 1.0 >> "${sv_file_prefix}_reliable.vcf"

echo "SV finished! Cleaning up..."




