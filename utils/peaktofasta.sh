
#!/bin/bash

ref=/oak/stanford/groups/akundaje/refs/mm10/GRCm38.p4.genome.fa
indir=/home/groups/akundaje/jelenter/ranked_peaks_thousand
outdir=/oak/stanford/groups/akundaje/projects/aav/explain_inputs/split_inputs

for file in  `ls $indir`
do
    inpeak=$indir/$file
    echo $inpeak
    outfasta=$outdir/$file
    echo $outfasta
    python peaktofasta.py --peaks $inpeak --outf $outfasta --ref_fasta $ref
done
