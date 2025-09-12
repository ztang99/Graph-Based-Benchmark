#!/bin/bash

#################################################################
# Step 6: Compress and Index Multiple VCF Files

## author: Nahyun Kong & Zitian Tang.
## contact: nahyun@wustl.edu & tang.zitian@wustl.edu
#################################################################

# Check input argument
if [ $# -ne 2 ]; then
    echo "Usage: $0 <refver>"
    echo "refver must be either 'hg38' or 'chm13'"
    exit 1
fi

# Variables
refver="$1"
workdir="$2"
sample_name="9188e8"
working_dir="${workdir}/${refver}"

# List of files to process
input_files=(
    "${working_dir}/${sample_name}_MSDeComp_comb_snvs_reliable_reform_filtergt.vcf"
    "${working_dir}/${sample_name}_MSDeComp_comb_indels_reliable_reform_filtergt.vcf"
    "${working_dir}/${sample_name}_MSDeComp_comb_svs_reliable_reform_filtergt.vcf"
)

# Process each file
for vcf_file in "${input_files[@]}"; do
    # Check if the VCF file exists
    if [ -f "$vcf_file" ]; then
        echo "Processing $vcf_file..."

        # Compress with bgzip
        vcf_gz_file="${vcf_file}.gz"
        echo "Compressing with bgzip..."
        bgzip -c "$vcf_file" > "$vcf_gz_file"

        # Index with tabix
        echo "Indexing with tabix..."
        tabix -p vcf "$vcf_gz_file"

        echo "Completed: $vcf_gz_file"
    else
        echo "File not found: $vcf_file"
    fi
done

echo "All files processed!"