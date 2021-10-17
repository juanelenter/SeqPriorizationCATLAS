import argparse
import pdb 
import pysam 
import numpy as np
import pandas as pd
from dragonn.vis import *
from kerasAC.splits import *
import math
from math import floor
import pdb
ltrdict = {'a':[1,0,0,0],
           'c':[0,1,0,0],
           'g':[0,0,1,0],
           't':[0,0,0,1],
           'n':[0,0,0,0],
           'A':[1,0,0,0],
           'C':[0,1,0,0],
           'G':[0,0,1,0],
           'T':[0,0,0,1],
           'N':[0,0,0,0]}


def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("--ref_fasta",default="/mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta")
    parser.add_argument("--snpinfo")
    parser.add_argument("--gkmexplain_prefix")
    parser.add_argument("--gkmexplain_suffix")
    parser.add_argument("--flank",type=int,default=500) 
    parser.add_argument("--outf_prefix")
    parser.add_argument("--plot_start_base",type=int,default=450)
    parser.add_argument("--plot_end_base",type=int,default=550)
    parser.add_argument("--snp_pos",type=int,default=501)    
    return parser.parse_args()

def plot_seq_importance(outf,tracks,labels,ylim,xlim,snp_pos, heatmap_indices=None, figsize=(75, 6)):
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 10}
    matplotlib.rc('font', **font)
    num_plots=len(tracks)
    f,axes=plt.subplots(nrows=3,ncols=10,dpi=80,figsize=figsize)
    show=False
    seq_len = tracks[0].shape[0]
    hmaps={}
    for plot_index in range(num_plots): 
        cur_track=tracks[plot_index]
        cur_snp_pos=snp_pos[plot_index]
        cur_ylim=ylim[plot_index]
        cur_xlim=xlim[plot_index]
        vmin=-1*max([abs(cur_ylim[0]),abs(cur_ylim[1])])
        vmax=max([abs(cur_ylim[0]),abs(cur_ylim[1])])
        if (heatmap_indices is not None) and (plot_index in heatmap_indices):
            extent=[cur_xlim[0],cur_xlim[1],0,400]
            hmap=axes[plot_index].imshow(cur_track[cur_xlim[0]:cur_xlim[1],:].T,extent=extent,vmin=vmin,vmax=vmax,interpolation='nearest',aspect='auto',cmap='seismic')
            hmaps[plot_index]=hmap
            axes[plot_index].set_yticks(np.array([100,200,300,400]))
            axes[plot_index].set_yticklabels(['T','G','C','A'])
        else:
            col=int(floor(plot_index/3))
            row=plot_index%3
            axes[row][col]=plot_bases_on_ax(cur_track,axes[row][col],show_ticks=True)
            axes[row][col].set_xlim(cur_xlim) 
            axes[row][col].set_ylim(cur_ylim)
        cur_label=labels[plot_index] 
        axes[row][col].set_title(cur_label)
        axes[row][col].axvline(x=cur_snp_pos,color='k',linestyle='--')
        axes[row][col].tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
    for hmap_index in hmaps:
        plt.colorbar(hmaps[hmap_index],ax=axes[hmap_index],orientation='horizontal')
    plt.subplots_adjust(hspace=0.5)
    plt.tight_layout()
    plt.savefig(outf,format='png',dpi=120)
    plt.close() 
    return 

def get_vals_from_gkm_line(seq):
    return np.asarray([[float(i) for i in i.split(',')] for i in seq.split(';')])

def one_hot_encode(seq):
    return np.array([ltrdict.get(x,[0,0,0,0]) for x in seq])


def get_seq(ref,chrom,pos,allele,flank):
    seq_prefix=ref.fetch(chrom,int(pos)-flank,int(pos)).upper() 
    seq_suffix=ref.fetch(chrom,int(pos)+1,int(pos)+flank).upper()
    #one-hot-encode the seq 
    return one_hot_encode(seq_prefix+allele.upper()+seq_suffix)


def main():
    args=parse_args()
    #load the gkmexplain data
    snps=pd.read_csv(args.snpinfo,header=0,sep='\t')
    toplot=snps['rsid'].tolist()
    toplot_dict={}
    for snp in toplot:
        toplot_dict[snp]=1
    print(toplot_dict)
    snp_to_vals={}
    ref=pysam.FastaFile(args.ref_fasta)
    for fold in range(10):
        noneffect=pd.read_csv(args.gkmexplain_prefix+"noneffect."+str(fold)+args.gkmexplain_suffix,header=None,sep='\t')
        effect=pd.read_csv(args.gkmexplain_prefix+"effect."+str(fold)+args.gkmexplain_suffix,header=None,sep='\t')
        print("loaded gkmexplain scores") 
        for index,row in noneffect.iterrows():
            cur_snp_info=row[0].split('_')
            rsid=cur_snp_info[4]
            if rsid not in toplot_dict:
                continue
            chrom=cur_snp_info[0]
            pos=int(cur_snp_info[1])
            allele=cur_snp_info[5]
            vals=get_vals_from_gkm_line(row[2])
            seq=get_seq(ref,chrom,pos,allele,args.flank)
            if rsid not in snp_to_vals: 
                snp_to_vals[rsid]={}
            if fold not in snp_to_vals[rsid]:
                snp_to_vals[rsid][fold]={} 
            snp_to_vals[rsid][fold]['noneffect_vals']=vals
            snp_to_vals[rsid][fold]['noneffect_allele']=allele
            snp_to_vals[rsid][fold]['noneffect_seq']=seq

        print("parsed noneffect allele seq + gkmexplain scores")
        for index,row in effect.iterrows():
            cur_snp_info=row[0].split('_')
            rsid=cur_snp_info[4]
            if rsid not in toplot_dict:
                continue
            chrom=cur_snp_info[0]
            pos=cur_snp_info[1]
            allele=cur_snp_info[5]
            vals=get_vals_from_gkm_line(row[2])
            seq=get_seq(ref,chrom,pos,allele,args.flank)
            snp_to_vals[rsid][fold]['effect_vals']=vals
            snp_to_vals[rsid][fold]['effect_allele']=allele
            snp_to_vals[rsid][fold]['effect_seq']=seq
        print("parsed effect allele seq + gkmexplain scores")

    for rsid in snp_to_vals:
        plot_wrapper(rsid,
                     effect_allele=[snp_to_vals[rsid][i]['effect_allele'] for i in range(10)],
                     effect_vals=[snp_to_vals[rsid][i]['effect_vals'] for i in range(10)],
                     effect_seq=[snp_to_vals[rsid][i]['effect_seq'] for i in range(10)],
                     noneffect_allele=[snp_to_vals[rsid][i]['noneffect_allele'] for i in range(10)],
                     noneffect_vals=[snp_to_vals[rsid][i]['noneffect_vals'] for i in range(10)],
                     noneffect_seq=[snp_to_vals[rsid][i]['noneffect_seq'] for i in range(10)],
                     args=args)
        
    
def plot_wrapper(rsid,effect_allele,effect_vals,effect_seq,noneffect_allele,noneffect_vals,noneffect_seq,args):
    png_title=args.outf_prefix+'/'+rsid+'.allfolds.png'
    toplot_tracks=[]
    toplot_labels=[]
    for i in range(10):
        effect_track=effect_vals[i]*effect_seq[i]
        noneffect_track=noneffect_vals[i]*noneffect_seq[i]
        delta_track=effect_track-noneffect_track
        toplot_tracks.append(effect_track)
        toplot_tracks.append(noneffect_track)
        toplot_tracks.append(delta_track)
        toplot_labels.append(rsid+' fold '+str(i)+' gkmexplain effect:'+effect_allele[i])
        toplot_labels.append(rsid+' fold '+str(i)+' gkmexplain noneffect:'+noneffect_allele[i])
        toplot_labels.append(rsid+' fold '+str(i)+' gkmexplain effect - noneffect:'+ effect_allele[i]+"-"+noneffect_allele[i])
        
    minvals=[]
    maxvals=[]
    
    #gkm y bounds 
    gkm_min=min([np.amin(i) for i in toplot_tracks])
    minvals=[gkm_min]*len(toplot_tracks)
    gkm_max=max([np.amax(i) for i in toplot_tracks])
    maxvals=[gkm_max]*len(toplot_tracks)

    ylim=[(minvals[i],maxvals[i]) for i in range(len(toplot_tracks))]
    xlim=[(args.plot_start_base,args.plot_end_base) for i in range(len(toplot_tracks))]
          
    snp_pos=[args.snp_pos for i in range(len(toplot_tracks))]
    plot_seq_importance(png_title,
                        toplot_tracks,
                        toplot_labels,
                        ylim=ylim,
                        xlim=xlim,
                        snp_pos=snp_pos,
                        heatmap_indices=None)
    
if __name__=="__main__":
    main()
    
