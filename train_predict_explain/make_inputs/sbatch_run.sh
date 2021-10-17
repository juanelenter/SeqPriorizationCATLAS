#!/bin/bash

outdir=/oak/stanford/groups/akundaje/projects/aav/svm_inputs
ref_fasta=/oak/stanford/groups/akundaje/refs/mm10/GRCm38.p4.genome.fa
genomewide_gc=/oak/stanford/groups/akundaje/soumyak/refs/mm10/gc_mm10_nosmooth.1k_win.500_stride.tsv
genome=mm10
ntrain=60000
chrom_sizes=mm10.chrom.sizes

[[ -d $outdir/logs ]] || mkdir $outdir/logs

cd /home/groups/akundaje/jelenter/SVM_pipelines/make_inputs

for task in CLAGL D1MSN D2MSN ITL6GL NPGL PTGL PVGA SSTGA VIPGA
do
    peaks=/oak/stanford/groups/akundaje/projects/aav/merged_narrowpeaks/$task.bed
    echo $peaks
    sbatch --export=ALL --requeue -J $task -o $outdir/logs/$task.o -e $outdir/logs/$task.e -t 1-0 --mem=60000 -p akundaje,owners run.sh $task $peaks $outdir $ref_fasta $genomewide_gc $genome $ntrain
done
