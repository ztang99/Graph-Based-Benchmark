#################################################################
# Step 2: separate SNVs, indels, and SVs in the in the combined VCF.

## author: Zitian Tang
## contact: tang.zitian@wustl.edu
#################################################################

import argparse

def split_by_var_type(input_file, snv_output_file=None, indel_output_file=None, sv_output_file=None):
    """
    Inputs:
        input_file: combined version VCF (that has SNVs, Indels, and/or SVs).
        snv_output_file: output file path for SNV VCF file (default: None).
        indel_output_file: output file path for Indel VCF file (default: None).
        sv_output_file: output file path for SV VCF file (default: None).
    """
    with open(input_file, 'r') as f_in:
        snv_out = open(snv_output_file, 'w') if snv_output_file else None
        indel_out = open(indel_output_file, 'w') if indel_output_file else None
        sv_out = open(sv_output_file, 'w') if sv_output_file else None

        for line in f_in:
            if line.startswith('#'):
                if snv_out:
                    snv_out.write(line)
                if indel_out:
                    indel_out.write(line)
                if sv_out:
                    sv_out.write(line)
                continue

            parts = line.strip().split('\t')
            ref = parts[3]
            alt = parts[4].split(',')[0]  ## now GT can be "GGTGT,*"

            abs_len_diff = abs(len(ref) - len(alt)) # length diff based on GIAB definition

            if len(ref) == 1 and len(alt) == 1:  # SNVs
                if snv_out:
                    snv_out.write('\t'.join(parts) + '\n')
            elif abs_len_diff < 50: # for v1.3 WG only: len(ref) < 50 and len(alt) < 50:  # v1.4: abs_len_diff < 50:
                if indel_out:
                    indel_out.write('\t'.join(parts) + '\n')
            else:  # SVs
                if sv_out:
                    sv_out.write('\t'.join(parts) + '\n')

        if snv_out:
            snv_out.close()
        if indel_out:
            indel_out.close()
        if sv_out:
            sv_out.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Split variants by their variant type')
    parser.add_argument('--refver', required=True, choices=['hg38', 'chm13'], help='Reference version (hg38 or chm13)')
    parser.add_argument('--workdir', required=True, help='Working directory')
    
    args = parser.parse_args()
    
    sample_name = '9188e8'
    working_dir = f'{args.workdir}/{args.refver}'
    
    ### v1.4.2 0228 ###
    input_file = f'{working_dir}/{sample_name}_MSDeComp_comb.vcf'
    snv_out = f'{working_dir}/{sample_name}_MSDeComp_comb_snvs.vcf'
    indel_out = f'{working_dir}/{sample_name}_MSDeComp_comb_indels.vcf'
    sv_out = f'{working_dir}/{sample_name}_MSDeComp_comb_svs.vcf'
    split_by_var_type(input_file, snv_output_file=snv_out, indel_output_file=indel_out, sv_output_file=sv_out)
