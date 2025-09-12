
#################################################################
# Step 5: filter genotypes to include only variants that are
# homozygous ref in HG005 and have at least one alt in others.

## author: Zitian Tang
## contact: tang.zitian@wustl.edu
#################################################################

import argparse

def extract_genotypes_from_info(info_field):
    """Extract genotypes from INFO field and return them as a dictionary."""
    genotypes = {}
    # Find the section containing genotypes
    for field in info_field.split(';'):
        if field.startswith('HG'):
            sample = field.split('=')[0].replace('_GT', '')
            gt = field.split('=')[1]
            genotypes[sample] = gt.replace('/', '|')  # Standardize separator
    return genotypes

def check_somatic_alleles(genotypes_dict):
    """Check if at least one of the alleles in the somatic samples is 1.
    Somatic samples are all samples except HG005."""
    somatic_samples = ['HG002', 'HG00438', 'HG02257', 'HG02486', 'HG02622']
    all_alleles = []
    
    # Collect all alleles from somatic samples
    for sample in somatic_samples:
        if sample in genotypes_dict:
            gt = genotypes_dict[sample]
            alleles = gt.split('|')
            all_alleles.extend([a for a in alleles if a != '.'])  # Skip missing alleles
    
    # Check if at least one allele is '1'
    return '1' in all_alleles

def filter_chr_and_gt(line):
    """
    Filter variants based on:
    1. HG005 GT must be 0|0 for chr1-22 or 0|./.|0 for chrX/Y
    2. At least one allele must be 1 in the somatic samples
    """
    # if line.startswith("#"):
    #     return True
    
    columns = line.strip().split("\t")
    chromosome = columns[0]
    info_field = columns[7]
    
    # Extract genotypes from INFO field
    genotypes = extract_genotypes_from_info(info_field)
    
    # Check HG005 genotype
    hg005_gt = genotypes.get('HG005')

    if chromosome.startswith("chr"):
        if chromosome[3:].isdigit():  # Autosomal chromosomes (chr1-22)
            ## 0318 v1.5 after * representing unknowns ##
            alleles = hg005_gt.split('|')
            if not all(allele in ['0', '*'] for allele in alleles): # unknowns are acceptable (*), initial gaps are not acceptable (.)
                return False
        elif chromosome in ["chrX", "chrY"]:  # Sex chromosomes
            if hg005_gt not in ["0|.", ".|0", "*|.", ".|*"]:
                return False
        
        # Check if at least one somatic sample has allele 1
        return check_somatic_alleles(genotypes)
    
    return False

def format_af_value(gt_af_field):
    """Extract and format AF value from the GT:AF field"""
    try:
        gt, af = gt_af_field.split(':')
        rounded_af = round(float(af), 4)
        return f"{gt}:{rounded_af}"
    except (ValueError, IndexError):
        return gt_af_field

def select_lines(input_file, output_file, filter_function):
    """Filter VCF file based on genotype information in INFO field."""
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if line.startswith("#"):
                f_out.write(line)
                continue
                
            if filter_function(line):
                columns = line.strip().split("\t")
                columns[-1] = format_af_value(columns[-1])
                f_out.write('\t'.join(columns) + '\n')
                # f_out.write(line)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Split variants by their variant type')
    parser.add_argument('--refver', required=True, choices=['hg38', 'chm13'], help='Reference version (hg38 or chm13)')
    parser.add_argument('--workdir', required=True, help='Working directory')
    
    args = parser.parse_args()
    
    sample_name = '9188e8'
    working_dir = f'{args.workdir}/{args.refver}'

    ### 1.4.2 0228 ###
    input_files = [
        f'{working_dir}/{sample_name}_MSDeComp_comb_snvs_reliable_reform.vcf',
        f'{working_dir}/{sample_name}_MSDeComp_comb_indels_reliable_reform.vcf',
        f'{working_dir}/{sample_name}_MSDeComp_comb_svs_reliable_reform.vcf'
    ]
    output_files = [
        f'{working_dir}/{sample_name}_MSDeComp_comb_snvs_reliable_reform_filtergt.vcf',
        f'{working_dir}/{sample_name}_MSDeComp_comb_indels_reliable_reform_filtergt.vcf',
        f'{working_dir}/{sample_name}_MSDeComp_comb_svs_reliable_reform_filtergt.vcf'
    ]
    
    select_lines(input_files[0], output_files[0], filter_chr_and_gt)
    select_lines(input_files[1], output_files[1], filter_chr_and_gt)
    select_lines(input_files[2], output_files[2], filter_chr_and_gt)
    
    
