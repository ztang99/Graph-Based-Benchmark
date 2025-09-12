#################################################################
# Step 5: combine the dot vcf and the zero vcf, labeling variants that differ between the two as '*'

## author: Andrew Ruttenberg
## contact: ruttenberg.andrew@wustl.edu
#################################################################

import argparse

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-d', '--dot', required=True, help='dot VCF')
    parser.add_argument('-z', '--zero', required=True, help='zero VCF')
    parser.add_argument('-t', '--header', required=True, help='header text file')
    parser.add_argument('-o', '--out', required=True, help='outfile')
    args = parser.parse_args()

    with open(args.out, 'w') as writeOut:
        with open(args.header, "r") as header:
            for line in header:
                writeOut.write(line)

        dotfile=open(args.dot, 'r')
        zerofile=open(args.zero, 'r')
        while True:
            dotLine=dotfile.readline()
            zeroLine=zerofile.readline()
            if dotLine=="" or zeroLine=="":
                break
            dotSplit=dotLine.strip().split()
            zeroSplit=zeroLine.strip().split()
            finalSplit=dotSplit

            for i in range(9, 20):
                if dotSplit[i]!=zeroSplit[i]:
                    finalSplit[i]='*'

            writeOut.write("\t".join(finalSplit)+"\n")

if __name__ == '__main__':
    main()
            
            



