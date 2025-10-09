#!/bin/bash
#SBATCH --job-name=repeatmasker.sh
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=30
#SBATCH --time=6-3:00:00
#SBATCH --output=./repeatmasker.log
#SBATCH --error=./repeatmasker.err
#SBATCH --mem=50G

cd /scratch/qfu/RepeatMasker/RepeatMasker

RepeatMasker -species human -dir /scratch/qfu/SMaHT_pangenome/trueset/ -a /scratch/qfu/SMaHT_pangenome/trueset/output_insertion.fasta