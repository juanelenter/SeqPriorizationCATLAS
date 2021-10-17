sbatch --export=ALL \
       --mem=10000 \
       --requeue \
       -t 02:00:00 \
       -p akundaje,owners,normal \
       -J importancetobw \
       -o /home/groups/akundaje/jelenter/SVM_pipelines/interpret/importance.o \
       -e /home/groups/akundaje/jelenter/SVM_pipelines/interpret/importance.e \
       importance_h5_to_bw.sh
