Traceback (most recent call last):
  File "importance_hdf5_to_bigwig_v2.py", line 25, in <module>
    f = np.load(args.scores, allow_pickle = 1)
  File "/home/groups/akundaje/jelenter/miniconda3/envs/svms/lib/python3.7/site-packages/numpy/lib/npyio.py", line 417, in load
    fid = stack.enter_context(open(os_fspath(file), "rb"))
FileNotFoundError: [Errno 2] No such file or directory: '/oak/stanford/groups/akundaje/projects/aav/explain_scores/NPGL/fold0/split_scores/NPGL.fold0.explain-all.npy'
