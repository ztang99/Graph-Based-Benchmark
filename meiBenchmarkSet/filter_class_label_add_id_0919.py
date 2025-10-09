#!/usr/bin/env python3
import argparse
import re
from collections import defaultdict

# Define the types we want to keep, including subtypes
young_l1 = {"L1HS", "L1PA2","L1P1"}
young_alu = {"AluY", "AluYa5", "AluYb8", "AluYb9","AluYf4", "AluYg6", "AluYc", "AluYa8","AluYd8","AluYk12","AluYk11","AluYh9","AluYk4"}
young_sva = {"SVA_F", "SVA_E", "SVA_D"}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Update VCF file with information from .out file.")
    parser.add_argument("out_file", help="Path to the .out file")
    parser.add_argument("vcf_file", help="Path to the .vcf file")
    parser.add_argument("output_file", help="Path to the filtered .out file")
    parser.add_argument("output_vcf_file", help="Path to the output .vcf file")
    parser.add_argument("mei_type", choices=["l1", "alu", "sva"], help="MEI type to filter: l1 or alu or sva")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Determine which types to keep
    if args.mei_type.lower() == "l1":
        types_to_keep = young_l1
    elif args.mei_type.lower() == "alu":
        types_to_keep = young_alu
    elif args.mei_type.lower() == "sva":
        types_to_keep = young_sva
    else:
        raise ValueError(f"Unknown mei_type '{args.mei_type}'.")

    # --- Parse .out and collect hits per ID ---
    out_data = {}
    with open(args.out_file, 'r') as infile, open(args.output_file, 'w') as outfile:
        lines = infile.readlines()[3:]  # Skip first three header lines (RepeatMasker .out)
        for raw in lines:
            cols = raw.split()
            if len(cols) < 11:
                continue
            id_line = cols[4].strip()
            query_start = cols[5].strip()
            query_end = cols[6].strip()
            repeat_class_subfamily = cols[9].strip()
            repeat_class = cols[10].strip()

            # Keep if subfamily starts with any target token
            if any(repeat_class_subfamily.startswith(k) for k in types_to_keep):
                outfile.write(raw)
                repeat_info = (repeat_class_subfamily, repeat_class, query_start, query_end)
                out_data.setdefault(id_line, [])
                if repeat_info not in out_data[id_line]:
                    out_data[id_line].append(repeat_info)

    # --- Prepare counters for IDs --- 
    global_id = 0                         # increments only when a NEW (chr, pos) appears (never resets per chrom)
    seen_positions = set()        
    chrpos_counter = defaultdict(int)    # per (chr,pos) ((chr,pos) -> count)

    # --- Update VCF ---
    with open(args.vcf_file, 'r') as vcf_in, open(args.output_vcf_file, 'w') as vcf_out:
        for line in vcf_in:
            if line.startswith('##'):
                vcf_out.write(line)
                continue

            if line.startswith('#CHROM'):
                # Add our custom header about the ID column
                vcf_out.write(
                    f"##ID_Description=<ID=VariantID,Description=\"3rd column (ID) formatted as "
                    f"{args.mei_type}_<global_id>_<chrom>_<pos>_<local_id>, "
                    "where <global_id> increments for each new (chrom,pos) across file, "
                    "<local_id> increments for each MEI split line within that (chrom,pos).\">\n"
                )
                # Existing INFO header
                vcf_out.write('##INFO=<ID=MEI,Number=1,Type=String,Description="MEI">\n')
                vcf_out.write(line)
                continue

            columns = line.rstrip('\n').split('\t')
            chrom, pos = columns[0], columns[1]
            chrom_pos_id_ref = '_'.join(columns[:4])
            # If we have RepeatMasker hits for this record, split into multiple rows (option4 logic)
            if chrom_pos_id_ref in out_data:
                # Safer INFO parse  # <<< NEW >>>
                info_fields = {}
                for fld in columns[7].split(';'):
                    if '=' in fld:
                        k, v = fld.split('=', 1)
                        info_fields[k] = v
                    else:
                        info_fields[fld] = ''

                # Optional SVLEN handling (not strictly needed for current logic)
                svlen = None
                svlen_str = info_fields.get("SVLEN")
                if svlen_str is not None:
                    try:
                        svlen = int(svlen_str)
                    except ValueError:
                        svlen = None

                dup_count = 0
                alt_orig = columns[4]
                if (chrom, pos) not in seen_positions:
                    global_id += 1
                    seen_positions.add((chrom, pos))

                for subfamily, repeat_class, start_s, end_s in out_data[chrom_pos_id_ref]:
                    dup_count += 1
                    # Keep only exact subfamilies if desired (you already filtered above by startswith)
                    if subfamily not in types_to_keep:
                        # If you want to keep startswith semantics here too, replace with:
                        # if not any(subfamily.startswith(k) for k in types_to_keep): continue
                        continue

                    # Copy original columns
                    new_columns = columns.copy()
                    # --- NEW ID: {mei_type}_{id}_{chr}_{pos}_{id2} ---
                    chrpos_counter[(chrom, pos)] += 1
                    new_columns[2] = f"{args.mei_type}_{global_id}_{chrom}_{pos}_{chrpos_counter[(chrom, pos)]}"
                    # Slice ALT to the sub-fragment [start:end] (1-based inclusive)
                    # with clamping to valid range  # <<< NEW >>>
                    try:
                        start = max(1, int(start_s))
                        end = int(end_s)
                    except ValueError:
                        # If start/end are not ints, skip this sub-hit
                        continue

                    if end < start:
                        continue

                    # Clamp to ALT length
                    alt_len = len(alt_orig)
                    if alt_len == 0:
                        continue
                    start0 = min(max(start - 1, 0), alt_len - 1)
                    end0 = min(max(end, 1), alt_len)  # slice is exclusive at end
                    sub_alt = alt_orig[0] + alt_orig[start0:end0]  # keep first base + insertion part

                    # Update ALT and INFO
                    new_columns[4] = sub_alt
                    mei_info = f"({repeat_class},{subfamily})"
                    if new_columns[7].endswith(';') or new_columns[7] == '':
                        new_columns[7] += f"MEI={mei_info}"
                    else:
                        new_columns[7] += f";MEI={mei_info}"
                    vcf_out.write('\t'.join(new_columns) + '\n')


if __name__ == '__main__':
    main()
