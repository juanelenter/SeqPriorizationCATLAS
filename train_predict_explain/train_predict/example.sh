#!/bin/bash


indir=/oak/stanford/groups/akundaje/projects/aav/svm_inputs
outdir=/oak/stanford/groups/akundaje/projects/aav/svm_training
lsgkm_dir=***Insert your lsgkm dir***

#for task in CLAGL D1MSN D2MSN ITL6GL NPGL PTGL PVGA SSTGA VIPGA 
for task in VIPGA
do
    echo $task
    [[ -d $outdir/logs ]] || mkdir $outdir/logs
    [[ -d $outdir/$task ]] || mkdir $outdir/$task
    [[ -d $outdir/$task/models ]] || mkdir $outdir/$task/models
    [[ -d $outdir/$task/predictions ]] || mkdir $outdir/$task/predictions

    for fold in {0..9}
    do
        echo $fold
        sbatch --export=ALL --time=24:00:00 --mincpus=16 --requeue -J $task -o $outdir/logs/$task.o -e $outdir/logs/$task.e --mem=60000 -p akundaje,owners /home/groups/akundaje/jelenter/SVM_pipelines/train_predict/train_predict.sh $task $fold $indir $outdir $lsgkm_dir 
    done
done
wait

