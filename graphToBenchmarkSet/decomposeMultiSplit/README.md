# decomposeMultiSplit

This directory holds code for variant decomposition and split multi-allelic sites.

## File Description and Run

Make sure to be in the correct code directory:
```bash
cd ./Graph-Based-Benchmark/graphToBenchmarkSet/decomposeMultiSplit
```
### 0_split_and_decompose.sh
This script runs the entirety of the multiallelic split and decomposition process.\
It takes in a graph VCF and an outdirectory to store all the intermidiate files/directorys and the file output.\
to run use the following command
```bash
bash 0_split_and_decompose.sh $graph_vcf $output_dir
```

### 1_multiallelic_split.sh
a bash script to run a multiallelic split on the graph twice, once labeling split sites as '.', once labeling them as '0'
To run this step:
```bash
bash 1_multiallelic_split.sh $graph_vcf $output_dir
```

### 2_split_graph.py
a python script to split the vcf into 12 different vcfs, one for each haplotype in the graph
To run this step:
```bash
python 2_split_graph.py -v graphVCF -o outdir
```

### 3_rtg_decompose.sh
a bash script to run a MNV decompsition on each of the hapotype vcfs
To run this step:
```bash
bash 3_rtg_decompose.sh $input_dir $output_dir
```

### 4_combine_and_sort.py
a python script that takes each of the 12 hapotypes from the graph and recombines them now that
the decomposition has been completed 
To run this step:
```bash
python 4_combine_and_sort.py -i input_dir -o output_vcf
```

### 5_combine_dot_and_zero.py
a python script to compare the '0' vcf to the '.'
it finds any variants that differ in the genotyping and labels them as '*'
To run this step:
```bash
python 5_combine_dot_and_zero.py -z zero_vcf -d dot_vcf -t header_for_output_vcf -o output_vcf
```
