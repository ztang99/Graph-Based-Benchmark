## 1. modify_vcf_id.py

reassign IDs to each VCF records

```jsx
python3 modify_vcf_id.py SMHTHAPMAP6_CHM13_v1.5_somatic_benchmark_svs.vcf SMHTHAPMAP6_CHM13_v1.6_somatic_benchmark_svs_out.vcf
```

    

## 2. create_fasta.py

generate fasta files containing all ALT sequences for insertions

```
python3 create_fasta.py SMHTHAPMAP6_GRCh38_v1.6_somatic_benchmark_svs_out.vcf
```
#> Number of sequences in the output: 
hg38 42163/ 
chm13: 34414


## 3. run repeat masker

- repeatMasker: RepeatMasker(v4.1.7), Search Engine: NCBI/RMBLAST [ 2.14.1+ ], Dfam (3.8)

```
RepeatMasker/RepeatMasker -species human -dir /storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/nahyun_tmp/mei_truthset/hg38/ -a /storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/nahyun_tmp/mei_truthset/hg38/output_insertion.fasta

```


## 4. young MEI selection & clipping

```bash
#hg38
#l1 
python3 filter_class_label_0430.py output_insertion.fasta.out SMHTHAPMAP6_GRCh38_v1.6_somatic_benchmark_svs_out.vcf output_insertion_young_l1.out SMHTHAPMAP6_GRCh38_v1.6_somatic_benchmark_mei_l1.vcf l1
#alu 
python3 filter_class_label_0430.py output_insertion.fasta.out SMHTHAPMAP6_GRCh38_v1.6_somatic_benchmark_svs_out.vcf output_insertion_young_alu.out SMHTHAPMAP6_GRCh38_v1.6_somatic_benchmark_mei_alu.vcf alu

#chm13 
#l1 
python3 filter_class_label_0430.py output_insertion.fasta.out SMHTHAPMAP6_CHM13_v1.6_somatic_benchmark_svs_out.vcf output_insertion_young_l1.out SMHTHAPMAP6_CHM13_v1.6_somatic_benchmark_mei_l1.vcf l1
#alu 
python3 filter_class_label_0430.py output_insertion.fasta.out SMHTHAPMAP6_CHM13_v1.6_somatic_benchmark_svs_out.vcf output_insertion_young_alu.out SMHTHAPMAP6_CHM13_v1.6_somatic_benchmark_mei_alu.vcf alu

```
