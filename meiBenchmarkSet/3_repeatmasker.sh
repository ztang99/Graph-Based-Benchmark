#BSUB -n 1
#BSUB -M 40G
#BSUB -R 'select[mem>40G && tmp>40G] rusage[mem=40GB,tmp=40GB] span[hosts=1]'
#BSUB -N
#BSUB -u nahyun@wustl.edu
#BSUB -G compute-jin810
#BSUB -J /storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/nahyun_tmp/mei_truthset/repeatmasker.sh
#BSUB -q general
#BSUB -oo /storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/nahyun_tmp/mei_truthset/repeatmasker.sh.log
#BSUB -a 'docker(veupathdb/repeatmasker:latest)'

RepeatMasker/RepeatMasker -species human -dir /storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/nahyun_tmp/mei_truthset/chm13/ -a /storage2/fs1/epigenome/Active/shared_smaht/TEST_RUN_FOLDER/TrueMutSet/nahyun_tmp/mei_truthset/chm13/output_insertion.fasta
