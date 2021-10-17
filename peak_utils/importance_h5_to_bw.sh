#!/bin/bash

for CELLTYPE in NPGL 
do
    scores=/oak/stanford/groups/akundaje/projects/aav/explain_scores/$CELLTYPE/fold0/split_scores/$CELLTYPE.fold0.explain-all.npy
    regions=/oak/stanford/groups/akundaje/projects/aav/explain_inputs/concat_peaks.tsv
    chrom_sizes=/home/groups/akundaje/jelenter/SVM_pipelines/make_inputs/mm10.chrom.sizes
    out_pfx=/oak/stanford/groups/akundaje/projects/aav/explain_scores/$CELLTYPE/fold0/split_scores/$CELLTYPE.fold0.explain-all

    python importance_hdf5_to_bigwig_v2.py \
        -sc $scores \
        -r $regions \
        -c $chrom_sizes \
        -o $out_pfx.bw \
        -s $out_pfx.stats.txt \
        -t 1
done
