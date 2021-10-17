#!/bin/bash
gkmexplain_prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/gkmexplain/outputs_from_gkmexplain/gkmexplain.
outf_prefix=/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/dopa_neurons_cluster_10/gkmexplain_plots
python plot_folds.py --snpinfo toplot.txt \
       --gkmexplain_prefix $gkmexplain_prefix \
       --gkmexplain_suffix .txt \
       --outf_prefix $outf_prefix \
       --flank 500 \
       --plot_start_base 400 \
       --plot_end_base 600 \
       --snp_pos 501

