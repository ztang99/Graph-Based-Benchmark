#!/usr/bin/env python3
#################################################################
## create_chrm_benchmarkset.py
##
## Reformat a combined VCF into a single chrM-only benchmark VCF:
## 1) Keep only chrM / MT / chrMT records
## 2) Reformat headers
## 3) Append calculated VAF field (HL)
##
## author: Nahyun Kong
## contact: nahyun@wustl.edu
#################################################################

import argparse


def calculate_vaf(gt_fields):
    total = 0.0
    hom = {0: 2, 1: 0.5, 2: 83.5, 3: 2, 4: 2, 5: 10}

    for i, gt in enumerate(gt_fields):
        a1, a2 = (a if a != '*' else '0' for a in gt.split('|'))
        if a1 == '0':
            continue
        total += hom[i]

    return str(total / 100.0)


def open_reformer(prefix):
    return open(f"{prefix}_mito.vcf", "w")


def write_header_line(line, fh):
    # drop unwanted contig lines
    if line.startswith("##contig=<ID=GRCh38#") or line.startswith("##contig=<ID=CHM13#"):
        return

    # replace AF block with HL and GT INFO fields
    if line.startswith('##INFO=<ID=AF'):
        block = [
            '##FORMAT=<ID=HL,Number=A,Type=Float,Description="Estimated allele frequency">',
            '##INFO=<ID=HG002_GT,Number=1,Type=String,Description="Genotype in HG002 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=HG00438_GT,Number=1,Type=String,Description="Genotype in HG00438 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=HG005_GT,Number=1,Type=String,Description="Genotype in HG005 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=HG02257_GT,Number=1,Type=String,Description="Genotype in HG02257 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=HG02486_GT,Number=1,Type=String,Description="Genotype in HG02486 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=HG02622_GT,Number=1,Type=String,Description="Genotype in HG02622 from maternal and paternal assemblies, second allele always .">',
            '##INFO=<ID=ORP,Number=1,Type=String,Description="Original position">',
            '##INFO=<ID=ORL,Number=1,Type=String,Description="Original ref length">',
        ]
        for b in block:
            fh.write(b + "\n")
        return

    # modify header to keep only one output sample column
    if line.startswith('#CHROM'):
        cols = line.rstrip('\n').split('\t')
        fh.write('\t'.join(cols[:9] + ['HapMap_Mixture']) + "\n")
        return

    fh.write(line)


def main():
    parser = argparse.ArgumentParser(
        description="Reformat combined VCF into a single chrM-only benchmark VCF"
    )
    parser.add_argument('-i', '--input', required=True, help="Combined input VCF")
    parser.add_argument('-o', '--output', required=True, help="Output filename prefix")
    args = parser.parse_args()

    fh = open_reformer(args.output)
    seen = set()

    with open(args.input) as fin:
        for line in fin:
            if line.startswith('#'):
                write_header_line(line, fh)
                continue

            cols = line.rstrip('\n').split('\t')

            # keep only chrM records
            if cols[0] not in ("chrM", "MT", "chrMT"):
                continue

            # safety check: expect at least 15 columns (9 fixed + 6 sample GTs)
            if len(cols) < 15:
                continue

            # rebuild INFO without AF, add per-sample GT tags
            info = [x for x in cols[7].split(';') if not x.startswith('AF=')]
            info += [
                f"HG002_GT={cols[9]}",
                f"HG00438_GT={cols[10]}",
                f"HG005_GT={cols[11]}",
                f"HG02257_GT={cols[12]}",
                f"HG02486_GT={cols[13]}",
                f"HG02622_GT={cols[14]}"
            ]

            # reset ID and QUAL
            cols[2], cols[5] = '.', '.'

            # compute output fields
            new_info = ';'.join(info)
            vaf = calculate_vaf(cols[-6:])
            out_cols = cols[:7] + [new_info, 'GT:HL', f"0/1:{vaf}"]

            # remove exact duplicate output rows
            key = tuple(out_cols)
            if key in seen:
                continue
            seen.add(key)

            fh.write('\t'.join(out_cols) + "\n")

    fh.close()
    print(f"Done. Created: {args.output}_mito.vcf")


if __name__ == '__main__':
    main()
