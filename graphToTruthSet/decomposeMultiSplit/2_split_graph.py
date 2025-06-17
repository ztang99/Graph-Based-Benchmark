#################################################################
# Step 2: Perform a splut the vcf by haplotype, allowing for
# RTG tools to decompose variants from each cell line

## author: Andrew Ruttenberg
## contact: ruttenberg.andrew@wustl.edu
#################################################################

import argparse

def main(): 

    """
    Input:
        vcf: path to input VCF file.
        outDir: path to output directory.
    """

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', '--vcf', required=True, help='sorted vcf of inputs')
    parser.add_argument('-o', '--outDir', required=True, help='output Directory')
    args = parser.parse_args()

    with open(args.vcf, "r") as f:
        head=[]
        outFiles=[]
        for line in f:
            # store all lines for the header to be used as the header of the output VCF
            if line.startswith("##"):
                head.append(line)
            elif line.startswith("#"):
                head.append(line)
                lineSplit=line.strip().split()
                for i in range(9, 21):
                    outFiles.append(open(f"{args.outDir}/{lineSplit[i]}.vcf", "w"))
                    for headLine in head:
                        outFiles[i-9].write(headLine)
            else:
                lineSplit=line.strip().split()
                # If varaint is present in a haplotype, write that line to the corosponding VCF output, otherwise skip it
                for i in range(9, 21):
                    if lineSplit[i]=='0' or lineSplit[i]=='.':
                        continue
                    elif lineSplit[i]=='1':
                        outFiles[i-9].write(line)
                    else:
                        print("ERR")
                        break



if __name__ == '__main__':
    main()