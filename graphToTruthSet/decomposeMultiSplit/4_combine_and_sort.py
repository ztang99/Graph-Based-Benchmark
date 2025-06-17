#################################################################
# Step 4: combine the cell line back into a single VCF

## author: Andrew Ruttenberg
## contact: ruttenberg.andrew@wustl.edu
#################################################################


import argparse

class vcfLine:
    def __init__(self, chrom, pos, ref, alt, line): 
        self.chrom=chrom
        self.pos=pos
        self.ref=ref
        self.alt=alt
        self.line=line

    def __eq__(self, other):
        if other==None:
            return False
        return self.chrom==other.chrom and self.pos==other.pos and self.ref==other.ref and self.alt==other.alt

    def __lt__(self, other):
        if self.chrom!=other.chrom:
            return self.chrom<other.chrom
        if self.pos!=other.pos:
            return self.pos<other.pos
        if self.ref!=other.ref:
            return self.ref<other.ref
        return self.alt<other.alt

    def __str__(self):
        return f"{self.chrom}:{self.pos}: {self.ref}->{self.alt}"

def main():
    
    """
    Input:
        inDir: path to directory of input vcfs, one for each haplotype
        outFile: path to output VCF file.
    """

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', '--inDir', required=True, help='sorted vcf of inputs')
    parser.add_argument('-o', '--outFile', required=True, help='output Directory')
    args = parser.parse_args()

    HG002Mat=f"{args.inDir}/HG002_mat_RTG_Decompose.txt"
    HG002Pat=f"{args.inDir}/HG002_pat_RTG_Decompose.txt"
    HG00438Mat=f"{args.inDir}/HG00438_mat_RTG_Decompose.txt"
    HG00438Pat=f"{args.inDir}/HG00438_pat_RTG_Decompose.txt"
    HG005Mat=f"{args.inDir}/HG005_mat_RTG_Decompose.txt"
    HG005Pat=f"{args.inDir}/HG005_pat_RTG_Decompose.txt"
    HG02257Mat=f"{args.inDir}/HG02257_mat_RTG_Decompose.txt"
    HG02257Pat=f"{args.inDir}/HG02257_pat_RTG_Decompose.txt"
    HG02486Mat=f"{args.inDir}/HG02486_mat_RTG_Decompose.txt"
    HG02486Pat=f"{args.inDir}/HG02486_pat_RTG_Decompose.txt"
    HG02622Mat=f"{args.inDir}/HG02622_mat_RTG_Decompose.txt"
    HG02622Pat=f"{args.inDir}/HG02622_pat_RTG_Decompose.txt"

    print("read files")
    cellLines=[HG002Mat, HG002Pat, HG00438Mat, HG00438Pat, HG005Mat, HG005Pat, HG02257Mat, HG02257Pat, HG02486Mat, HG02486Pat, HG02622Mat, HG02622Pat]
    masterArray=[]
    for i in range(12):
        masterArray.append([None, open(cellLines[i], 'r')])
        line=masterArray[i][1].readline()
        lineSplit=line.strip().split()
        masterArray[i][0]=vcfLine(lineSplit[0], int(lineSplit[1]), lineSplit[3], lineSplit[4], line)

    it=0
    with open(args.outFile, 'w') as writeOut:
        currentVar=None
        while True:
            it+=1 
            if it%100000==0:    
                print(f"it:{it}")
            minVar=None

            for i in range(12):
                if masterArray[i][0]==None:
                    continue
                if minVar==None:
                    minVar=masterArray[i]
                elif masterArray[i][0]<minVar[0]:
                    minVar=masterArray[i]


            if minVar==None:
                break
            
            if currentVar==None:
                currentVar=minVar[0]

            elif currentVar==minVar[0]:
                currentVarSplit=currentVar.line.strip().split()
                minVarSplit=minVar[0].line.strip().split()
                for i in range(9, 20):
                    if currentVarSplit[i]==minVarSplit[i]:
                        continue
                    elif currentVarSplit[i]==".":
                        currentVarSplit[i]=minVarSplit[i]
                    elif minVarSplit[i]=='.':
                        continue
                    else:
                        currentVarSplit[i]=str(int(currentVarSplit[i])+int(minVarSplit[i]))
                currentVar.line="\t".join(currentVarSplit)

            else:
                if currentVar.line.endswith('\n'):
                    writeOut.write(currentVar.line)
                else:
                    writeOut.write(currentVar.line + "\n")
                currentVar=minVar[0]

            nextLine=minVar[1].readline()
            if nextLine=="":
                minVar[0]=None
            else:
                nextLineSplit=nextLine.strip().split()
                minVar[0]=vcfLine(nextLineSplit[0], int(nextLineSplit[1]), nextLineSplit[3], nextLineSplit[4], nextLine)


if __name__ == '__main__':
    main()

            





            





