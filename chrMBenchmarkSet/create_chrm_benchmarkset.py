#!/usr/bin/env python3
#################################################################
## create_chrm_benchmarkset.py
##
## 1) Split a combined VCF into SNV, indel, merged small (SNV+indel), and SV VCFs.
## 2) Reformat headers and append a calculated VAF field (labeled HL).
##
## author: Nahyun Kong 
## contact: nahyun@wustl.edu
#################################################################

import argparse

def calculate_vaf(gt_fields):
    total = 0.0
    # only homozygous-alt contributes now
    hom = {0:2, 1:0.5, 2:2, 3:2, 4:2, 5:10}
    for i, gt in enumerate(gt_fields):
        a1, a2 = (a if a!='*' else '0' for a in gt.split('|'))
        if a1 == '0':
            continue
        total += hom[i]
    return str(total / 100.0)

def open_reformers(prefix):
    """Open four output files in cwd using prefix."""
    return {
        'snv':   open(f"{prefix}.snvs.reform.vcf",   'w'),
        'indel': open(f"{prefix}.indels.reform.vcf", 'w'),
        'small': open(f"{prefix}.small.reform.vcf",  'w'),
        'sv':    open(f"{prefix}.svs.reform.vcf",    'w'),
    }, { key: False for key in ('snv','indel','small','sv') }

def write_header_line(line, fh, is_sv):
    """Write a header line (possibly transformed) to one reform file."""
    # drop unwanted contig lines
    if line.startswith("##contig=<ID=GRCh38#") or line.startswith("##contig=<ID=CHM13#"):
        return

    # replace AF block with HL and GT INFO
    if line.startswith('##INFO=<ID=AF'):
        block = [
            '##FORMAT=<ID=HL,Number=A,Type=Float,Description="Estimated allele frequency">',
            '##INFO=<ID=HG002_GT,Number=1,Type=String,Description="Genotype in HG002 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=HG00438_GT,Number=1,Type=String,Description="Genotype in HG00438 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=HG005_GT,Number=1,Type=String,Description="Genotype in HG005 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=HG02257_GT,Number=1,Type=String,Description="Genotype in HG02257 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=HG02486_GT,Number=1,Type=String,Description="Genotype in HG02486 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=HG02622_GT,Number=1,Type=String,Description="Genotype in HG02622 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=ORP,Number=1,Type=String,Description="Original position before splitting">',
            '##INFO=<ID=ORL,Number=1,Type=String,Description="Original ref length before splitting">',
        ]
        if is_sv:
            block += [
                '##INFO=<ID=SVTYPE,Number=1,Type=String,Description="SV type: DEL or INS">',
                '##INFO=<ID=SVLEN,Number=.,Type=Integer,Description="Difference in length between REF and ALT">'
            ]
        for b in block:
            fh.write(b + "\n")
        return

    # modify main header line to add HapMap_Mixture field
    if line.startswith('#CHROM'):
        cols = line.rstrip('\n').split('\t')
        fh.write('\t'.join(cols[:9] + ['HapMap_Mixture']) + "\n")
        return

    # all other header lines pass through
    fh.write(line)

def classify(ref, alt):
    """Classify a record as 'snv', 'indel', or 'sv'."""
    diff = abs(len(ref) - len(alt))
    if len(ref) == 1 and len(alt) == 1:
        return 'snv'
    if diff < 50:
        return 'indel'
    return 'sv'

def main():
    parser = argparse.ArgumentParser(
        description="Split & reformat combined VCF into SNV, indel, small (SNV+indel), and SV")
    parser.add_argument('-i', '--input',  required=True, help="Combined VCF")
    parser.add_argument('-o', '--output', required=True, help="Output filename prefix")
    args = parser.parse_args()

    fhs, header_done = open_reformers(args.output)

    with open(args.input) as fin:
        for line in fin:
            if line.startswith('#'):
                # broadcast header to all four outputs
                for var, fh in fhs.items():
                    write_header_line(line, fh, var == 'sv')
                # once we hit the #CHROM line, mark headers done
                if line.startswith('#CHROM'):
                    for k in header_done:
                        header_done[k] = True
                continue

            cols = line.rstrip('\n').split('\t')
            ref, alt = cols[3], cols[4].split(',')[0]
            var = classify(ref, alt)

            # rebuild INFO without AF, add per‐sample GT tags
            info = [x for x in cols[7].split(';') if not x.startswith('AF=')]
            info += [
                f"HG002_GT={cols[9]}", f"HG00438_GT={cols[10]}",
                f"HG005_GT={cols[11]}", f"HG02257_GT={cols[12]}",
                f"HG02486_GT={cols[13]}", f"HG02622_GT={cols[14]}"
            ]

            # for SVs, append SVTYPE and SVLEN
            if var == 'sv':
                svlen = len(alt) - len(ref)
                if abs(svlen) >= 50:
                    info.append(f"SVTYPE={'INS' if svlen > 0 else 'DEL'}")
                    info.append(f"SVLEN={abs(svlen)}")

            # reset ID & QUAL, assemble new INFO, compute VAF
            cols[2], cols[5] = '.', '.'
            new_info = ';'.join(info)
            vaf = calculate_vaf(cols[-6:])
            out_cols = cols[:7] + [new_info, 'GT:HL', f"0/1:{vaf}"]
            record = '\t'.join(out_cols) + "\n"

            # write to type-specific file
            fhs[var].write(record)
            # if SNV or indel, also write to merged small file
            if var in ('snv', 'indel'):
                fhs['small'].write(record)

    # close all files
    for fh in fhs.values():
        fh.close()

    # report
    print("Done. Created:")
    print(f"  {args.output}.snvs.reform.vcf")
    print(f"  {args.output}.indels.reform.vcf")
    print(f"  {args.output}.small.reform.vcf")
    print(f"  {args.output}.svs.reform.vcf")

if __name__ == '__main__':
    main()
