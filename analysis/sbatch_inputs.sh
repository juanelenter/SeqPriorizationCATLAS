#!/bin/bash

indir=/oak/stanford/groups/akundaje/projects/aav/explain_inputs
file=concat_peaks.fasta
lines_per_file=40
cp $indir/$file $indir/split_inputs/$file
cd $indir/split_inputs
split -d -l $lines_per_file -a 3 $file $file-
rm $file
