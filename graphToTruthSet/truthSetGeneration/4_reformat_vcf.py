#################################################################
# Step 4: reformat VCF headers.

## author: Nahyun Kong & Zitian Tang.
## contact: nahyun@wustl.edu & tang.zitian@wustl.edu
#################################################################

import argparse
import sys
from pathlib import Path

def calculate_vaf(columns):
    """Calculate expected VAF from genotype columns."""
    gt = [col for col in columns if col != '']
    gt = gt[-6:]
    if any('.' in gt[i] for i in [0, 1, 3, 4, 5]):
        return '.'

    expected_VAF = 0
    for col in [0, 1, 3, 4, 5]:
        col_val = gt[col]
        # * stands for "not ref and not alt"; but is considered as 0s when calculating VAF
        alleles = [a if a != '*' else '0' for a in col_val.split('|')]
        
        if '|'.join(alleles) != '0|0': # prev: col_val != '0|0':
            if (alleles[0] == '0' and alleles[1] != '0') or (alleles[0] != '0' and alleles[1] == '0'):  # Heterozygous variant
                if col in [0, 3, 4]: # hg002, hg02257, hg02486
                    expected_VAF += 1 
                if col == 5:          # hg02622
                    expected_VAF += 5 
                if col == 1:          # hg00438
                    expected_VAF += 0.25 
            elif (alleles[0] == alleles[1] and alleles[0] != '0'):  # Homozygous variant
                if col in [0, 3, 4]: # hg002, hg02257, hg02486
                    expected_VAF += 2
                if col == 5:          # hg02622
                    expected_VAF += 10
                if col == 1:          # hg00438
                    expected_VAF += 0.5
    expected_VAF = expected_VAF/100
    return expected_VAF

def process_and_reformat_vcf(input_path, output_path, SV):
    """Process VCF file to reformat and calculate VAF."""
    try:
        with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
            for line in infile:
                if line.startswith('#'):
                    if line.startswith("##INFO=<ID=AF"):
                        outfile.write('''##FORMAT=<ID=AF,Number=A,Type=Float,Description="Estimated allele frequency of the 6MAHPMAP Mixture in the range (0,1]">
##INFO=<ID=HG002_GT,Number=1,Type=String,Description="Genotype in HG002; * = Unknown individual-level GTs due to Multiallelic Split">
##INFO=<ID=HG00438_GT,Number=1,Type=String,Description="Genotype in HG00438; * = Unknown individual-level GT due to Multiallelic Split">
##INFO=<ID=HG005_GT,Number=1,Type=String,Description="Genotype in HG005; * = Unknown individual-level GT due to Multiallelic Split">
##INFO=<ID=HG02257_GT,Number=1,Type=String,Description="Genotype in HG02257; * = Unknown individual-level GT due to Multiallelic Split">
##INFO=<ID=HG02486_GT,Number=1,Type=String,Description="Genotype in HG02486; * = Unknown individual-level GT due to Multiallelic Split">
##INFO=<ID=HG02622_GT,Number=1,Type=String,Description="Genotype in HG02622; * = Unknown individual-level GT due to Multiallelic Split">
##INFO=<ID=ORP,Number=1,Type=String,Description="Original variant position after multiallelic split but before decomposing complex variants.">
##INFO=<ID=ORL,Number=1,Type=String,Description="Original reference length after multiallelic split but before decomposing complex variants.">\n''')
                        if SV:
                            outfile.write('''##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of SV:DEL=Deletion, INS=Insertion">
##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT alleles">\n''')
                    elif line.startswith('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tHG002'):
                        header_columns = line.strip().split("\t")
                        header_columns = header_columns[:9] + ["HapMap_Mixture"]
                        outfile.write('\t'.join(header_columns) + '\n')
                    elif line.startswith("##contig=<ID=GRCh38#") or line.startswith("##contig=<ID=CHM13#"):
                        continue
                    else:
                        outfile.write(line)
                    continue

                fields = line.strip().split("\t")
                
                info_fields = fields[7].split(';')
                new_info_fields = [field for field in info_fields if not field.startswith('AF=')]
                ## 0318 new version—GTs already handled by -m two versions so no need to replace genotypes ##
                sample_genotypes = [
                    f"HG002_GT={fields[9]}", 
                    f"HG00438_GT={fields[10]}", 
                    f"HG005_GT={fields[11]}",
                    f"HG02257_GT={fields[12]}", 
                    f"HG02486_GT={fields[13]}", 
                    f"HG02622_GT={fields[14]}"
                ]
                genotype_info = ';'.join(sample_genotypes)
                
                # Modify ID and QUAL fields
                fields[2] = "."
                fields[5] = "."
                # Construct output fields using original fields
                output_fields = fields[:7]
                if SV:
                    sv_length = len(output_fields[4]) - len(output_fields[3])
                    if abs(sv_length) < 50: #snvs and indels
                        output_fields.append(';'.join(new_info_fields) + ';' + genotype_info)  # Modified INFO
                    elif abs(sv_length) >= 50: #actual SVs
                        if sv_length > 0:
                            output_fields.append(';'.join(new_info_fields) + f';SVTYPE=INS;SVLEN={sv_length};{genotype_info}')
                        elif sv_length < 0:
                            output_fields.append(';'.join(new_info_fields) + f';SVTYPE=DEL;SVLEN={abs(sv_length)};{genotype_info}')
                else: # for rmSV, no SVs are included
                    output_fields.append(';'.join(new_info_fields) + ';' + genotype_info)  # Modified INFO

                output_fields.append("GT:AF")  # FORMAT

                # Calculate VAF using modified genotypes
                af = calculate_vaf(fields)
                
                # Create final output line with 0/1 GT and calculated AF
                data_column = f"0/1:{af}"
                output_fields.append(data_column)

                outfile.write('\t'.join(output_fields) + '\n')


    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e.filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Process and reformat VCF files.')
    parser.add_argument('--refver', default='hg38', help='Reference version (default: hg38), or chm13')
    parser.add_argument('--workdir', required=True, help='Working directory')

    args = parser.parse_args()
    sample_name = '9188e8'
    working_dir = f'{args.workdir}/{args.refver}'

    #load raw graph file for tracking multiallelic sites
    if args.refver == 'hg38':
        # input_file = f'/storage2/fs1/epigenome/Active/shared_smaht/SMaHT_MCGB_Graphs/contigs/{sample_name}/{sample_name}.vcf'
        raw_file = f'/storage2/fs1/epigenome/Active/shared_smaht/SMaHT_MCGB_Graphs/contigs/{sample_name}/{sample_name}.vcf'
    elif args.refver == 'chm13':
        raw_file = f'/storage2/fs1/epigenome/Active/shared_smaht/SMaHT_MCGB_Graphs/contigs/{sample_name}-CHM13/{sample_name}.vcf'
    # load vcf to update
    input_files = [
        f'{working_dir}/{sample_name}_MSDeComp_comb_snvs_reliable.vcf',
        f'{working_dir}/{sample_name}_MSDeComp_comb_indels_reliable.vcf',
        f'{working_dir}/{sample_name}_MSDeComp_comb_svs_reliable.vcf'
    ]
    
    output_files = [
        f'{working_dir}/{sample_name}_MSDeComp_comb_snvs_reliable_reform.vcf',
        f'{working_dir}/{sample_name}_MSDeComp_comb_indels_reliable_reform.vcf',
        f'{working_dir}/{sample_name}_MSDeComp_comb_svs_reliable_reform.vcf'
    ]

    ## 0318 new version with GT handled ##
    process_and_reformat_vcf(input_files[0], output_files[0], SV=False)  # SNVs
    process_and_reformat_vcf(input_files[1], output_files[1], SV=False)  # indels
    process_and_reformat_vcf(input_files[2], output_files[2], SV=True)   # SVs - fixed from incorrect index


if __name__ == "__main__":
    main()
