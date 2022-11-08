import numpy as np
import glob
from tabulate import tabulate
import pandas as pd
import h5py as h5
from os import walk
from IPython.display import clear_output


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
        self.measures=[]
        self.attribs = []
        self.lab = lab
    
        self.path = self.path+'/'+self.lab
        for folders in glob.glob(self.path+'/*'):
             self.folder_samples.append(folders)

        dsets = []
        for (dirpath, dirnames, filenames) in walk(self.path):
            if self.sample in dirpath:
                clear_output(wait=True)
                self.namef=[]
                for name in sorted(glob.glob(dirpath+'/*.h5')):
                    self.datac=[]
                    if self.exptype in name:
                        self.measures.append(name.split('/')[-1])
                        self.namef.append(name)
                        opendat = h5.File(name,'r')
                        attr_dict={}
                        for iset in opendat.keys():
                            dsets.append(iset)
                            for jset in opendat[iset].keys():
                                 self.datac.append(np.array(opendat[iset][jset]))
                                 for attr in opendat[iset][jset].attrs.keys():
                                    attr_dict[attr]= opendat[iset][jset].attrs[attr]
                        self.attribs.append(attr_dict)                    
                    self.data.append(self.datac)
                    self.filesname.append(self.namef)
                    self.pathname.append(dirpath)
                    self.ptable.append([self.count,self.measures[-1]])
                    self.count+=1
                
        if (self.datac and self.printtable==True):
            print(tabulate(self.ptable,self.headers,tablefmt="github",colalign=("center","left")))
    
        self.dframe = pd.DataFrame(self.ptable,columns=self.headers)
    

    def afm_nsom_data(self,measure):
        afm_nsom_data =  self.data[measure][0]
        afm          =   afm_nsom_data[:,:,0]
        lockin       =   afm_nsom_data[:,:,1]
        multimeter   =   afm_nsom_data[:,:,2]
        return afm, lockin, multimeter
    
    def exps_attr(self,measure):
        return self.attribs[measure]

    def amp_fase_data(self,measure):
        try:
             amplitud = self.data[measure][1]
             fase     = self.data[measure][2]
             return amplitud, fase
        except:
             return None
       
  

