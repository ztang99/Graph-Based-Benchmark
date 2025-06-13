
#################################################################
# Step 1: combine haplotypes from maternal and paternal sides.

## author: Zitian Tang
## contact: tang.zitian@wustl.edu
#################################################################

import re
import argparse

def combine_haplotype(input_file, output_file, sv_output_file=None, combined=False, excludeSV=False):
    """
    Input:
        input_file: path to input VCF file.
        output_file: path to output VCF file.
        sv_output_file: path to output file for SVs (optional).
        combined: whether the input VCF file already has combined haplotypes/genotypes. (default: False)
        excludeSV: whether to separate SVs into a different file (default: False)
    """
    # v1.4.1 new 0211
    sv_out = open(sv_output_file, 'w') if (sv_output_file and excludeSV) else None
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if line.startswith('#CHROM'):
                if not combined:
                    new_header = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tHG002\tHG00438\tHG005\tHG02257\tHG02486\tHG02622\n'
                    f_out.write(new_header)
                    continue
            
            if line.startswith('#'):
                f_out.write(line)
                continue
            
            # parts = line.strip().split('\t')
            parts = re.split(r'\s+', line.strip())
            ref = parts[3]
            alt = parts[4].split(',')
            samples = parts[9:]
            
            abs_len_diff = max(abs(len(ref) - len(alt_allele)) for alt_allele in alt)
            # v1.4.1 wrong definition of abs_len_diff
            # longest_alt = max(alt, key=len)
            # abs_len_diff = abs(len(ref) - len(longest_alt))

            # Version 1.4.1 remove SVs
            # if excludeSV:
            #     if abs_len_diff >= 50:
            #         continue
                # Version 1.3 SV length definition
                # if len(ref) >= 50:
                #     continue
                # if any(len(allele) >= 50 for allele in alt):
                #     continue
            
            if not combined:
                combined_samples = []
                for i in range(0, len(samples), 2):
                    maternal = samples[i]
                    paternal = samples[i + 1]
                    combined_mp = f'{maternal}|{paternal}'
                    combined_samples.append(combined_mp)

                parts[9:] = combined_samples

            # Version 1.4.1 new 0211 output removed SVs as well
            if excludeSV and abs_len_diff >= 50:
                if sv_out:
                    sv_out.write('\t'.join(parts) + '\n')
            else:
                f_out.write('\t'.join(parts) + '\n')

            # f_out.write('\t'.join(parts) + '\n')

    if sv_out:
        sv_out.close()
    f_in.close()
    f_out.close()


def main():
    parser = argparse.ArgumentParser(description='Step 1: combine haplotypes')
    parser.add_argument('--refver', required=True, choices=['hg38', 'chm13'], help='Reference version (hg38 or chm13)')
    parser.add_argument('--workdir', required=True, help='Working directory')
    parser.add_argument('--input-file', required=True, help='Multi-split, decomposed VCF file')
    
    args = parser.parse_args()
    
    sample_name = '9188e8'
    working_dir = f'{args.workdir}/{args.refver}'

    ## v1.4.2 new 0228
    out_combined = f'{working_dir}/{sample_name}_MSDeComp_comb.vcf' 
    combine_haplotype(args.input_file, out_combined, combined=False, excludeSV=False)

if __name__ == "__main__":
    main()

