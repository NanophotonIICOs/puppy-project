import os
import glob
from tabulate import tabulate
from datetime import date
import pandas as pd
import numpy as np
import h5py as h5
from os import walk
from IPython.display import display, clear_output
import math 

class experiments:
    def __init__(self,lab,exptype,sample,printtable=True):
        self.path='/media/labfiles/lab-exps'
        self.headers=['No. Dir','Name Dir']
        self.count=0
        self.foldername=[]
        self.filesname=[]
        self.pathname=[]
        self.ptable=[]
        self.datac=[]
        self.data=[]
        self.exptype=exptype
        self.printtable=printtable
        self.dirnames=[]
        self.folder_samples=[]
        self.sample = sample
        self.alldata=[]
        self.measures=[]
    
        self.path = self.path+'/'+lab
        for folders in glob.glob(self.path+'/*'):
             self.folder_samples.append(folders)

        for (dirpath, dirnames, filenames) in walk(self.path):
            if self.sample in dirpath:
                clear_output(wait=True)
                self.datac=[]
                self.namef=[]
                dsets = []
                for name in sorted(glob.glob(dirpath+'/*.h5')):
                    if self.exptype in name:
                        self.measures.append(name.split('/')[-1])
                        self.namef.append(name)
                        opendat = h5.File(name,'r')
                        for iset in opendat.keys():
                            dsets.append(iset)
                            for jset in opendat[iset].keys():
                                 self.datac.append(np.array(opendat[iset][jset]))
                    self.data.append(self.datac)
                    self.filesname.append(self.namef)
                    self.pathname.append(dirpath)
                    self.ptable.append([self.count,self.measures[0]])
                    self.count+=1
                
        if (self.datac and self.printtable==True):
            print(tabulate(self.ptable,self.headers,tablefmt="github",colalign=("center","left")))
    
        self.dframe = pd.DataFrame(self.ptable,columns=self.headers)

                    
class afm_nsom:
    def __init__(self,alldata,measure):
        self.alldata=alldata
        self.measure = measure
        self.afm_nsom_data = self.alldata[self.measure][0]
        self.amplitud = self.alldata[self.measure][1]
        self.fase = self.alldata[self.measure][2]
        self.xi=0;self.xf=self.afm_nsom_data.shape[1]
        self.yi=0;self.yf=self.afm_nsom_data.shape[0]
        self.afm         = self.afm_nsom_data[:,:,0]
        self.lockin      =  self.afm_nsom_data[:,:,1]
        self.multimeter  =  self.afm_nsom_data[:,:,2]



def new_axislabels(ax,step):
    newlabels=[labels*step for labels in ax.get_xticks().tolist()]
    return newlabels

def nsom_minoff(z,minoff):
    mo = math.floor(math.log(abs(z.min()), 10))
    minz = float("%fe%d"%(z.min(),mo))
    mominz = float("1e%d"%(mo))
    return  (minoff*mominz)


