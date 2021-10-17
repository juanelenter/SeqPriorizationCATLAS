import random
import pickle
import argparse
import pysam
import pandas as pd
import pdb
random.seed(1234)

def parse_args():
    parser=argparse.ArgumentParser(description="form svm inputs")
    parser.add_argument("--outf",nargs="+")
    parser.add_argument("--ref_fasta")
    parser.add_argument("--peaks",nargs="+")
    return parser.parse_args()

def main():
    args=parse_args()
    ref=pysam.FastaFile(args.ref_fasta)

    print("loaded negatives")
    for i in range(len(args.peaks)):
        cur_peaks=args.peaks[i]
        cur_outf=args.outf[i]
        print("cur_peaks:"+cur_peaks)
        print("cur_outf:"+cur_outf)

        outf_pos=open(cur_outf, 'w')

        cur_peaks=pd.read_csv(cur_peaks, sep='\t')
        print("loaded peaks for task")
        for index,row in cur_peaks.iterrows():
            if index%100==0:
                print(index)
            chrom=row['chr']
            start=row['start']
            end=row['end']
            seq=ref.fetch(chrom, start, end)
            header='_'.join([str(i) for i in [chrom,start,end,row['peak']]])
            outf_pos.write('>'+header+'\n'+seq+'\n')
        outf_pos.close()

if __name__=="__main__":
    main()
