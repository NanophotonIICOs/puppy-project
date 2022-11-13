import numpy as np
from glob import glob
from tabulate import tabulate
import pandas as pd
import h5py as h5
from os import walk
from IPython.display import clear_output

class experiments:
    def __init__(self,lab,exptype,sample,printtable=False):
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
        self.sample_names=[]
    
        self.path = self.path+'/'+self.lab
        for folders in glob(self.path+'/*'):
             self.folder_samples.append(folders)

        for (dirpath, dirnames, filenames) in walk(self.path):
            self.namef=[]
            if self.sample in dirpath:
                clear_output(wait=True)
                dsets = []
                clean_meas=[]
                for name in sorted(glob(dirpath+'/*.h5')):
                    if self.exptype in name:
                        self.sample_names.append(name)
                        self.measures.append(name.split('/')[-1])
                        self.namef.append(name)
                        opendat = h5.File(name,'r')
                        attr_dict={}
                        self.datac=[]
                        for iset in opendat.keys():
                            dsets.append(iset)
                            if len(list(opendat.keys()))>1:
                                for jset in opendat[iset].keys():
                                    self.datac.append(np.array(opendat[iset][jset]))
                                    for attr in opendat[iset][jset].attrs.keys():
                                        attr_dict[attr]= opendat[iset][jset].attrs[attr]
                            else:
                                self.datac.append(np.array(opendat[iset]))
                                try:
                                    for attr in opendat[iset].attrs.keys():
                                        attr_dict[attr]= opendat[iset].attrs[attr]
                                except:
                                    pass                       
                            
                        self.attribs.append(attr_dict)                     
                        self.data.append(self.datac)
                        self.ptable.append([self.count,self.measures[-1]])
                        self.pathname.append(dirpath)
                        self.count+=1
                self.filesname.append(self.namef)
        # if (self.datac or self.printtable==True):
        #     print(tabulate(self.ptable,self.headers,tablefmt="github",colalign=("center","left")))
        if (self.printtable==True):
            print(tabulate(self.ptable,self.headers,tablefmt="github",colalign=("center","left")))
    
        self.dframe = pd.DataFrame(self.ptable,columns=self.headers)
        self.meas_list=self.dframe['Name Dir'].tolist()
    

    def afm_nsom_data(self,measure):
        try:
            afm_nsom_data =  self.data[measure][0]
            afm          =   afm_nsom_data[:,:,0]
            lockin       =   afm_nsom_data[:,:,1]
            multimeter   =   afm_nsom_data[:,:,2]
            return afm, lockin, multimeter
            
        except IndexError:
            return self.data[measure][0]
            
        
    
    def exps_attr(self,measure):
        return self.attribs[measure]

    def amp_fase_data(self,measure):
        try:
             amplitud = self.data[measure][1]
             fase     = self.data[measure][2]
             return amplitud, fase
        except:
             return None
       
  



class get_data:
    def __init__(self,lab,exptype,sample,printtable=False,**kwargs):
        self.path='/media/labfiles/lab-exps'
        self.headers=['No. Dir','Name Dir']
        self.exptype=exptype
        self.printtable=printtable
        self.sample = sample
        self.lab = lab
        self.folder_samples=[]
        self.exp_meas=[]
        self.name_meas=[]
    
        self.path = self.path+'/'+self.lab
        for folders in glob(self.path+'/*'):
             self.folder_samples.append(folders)

        for (dirpath, dirnames, filenames) in walk(self.path):
            if self.sample in dirpath:
                clear_output(wait=True)
                for name in sorted(glob(dirpath+'/*.h5')):
                    if self.exptype in name:
                        self.exp_meas.append(name)
                        self.name_meas.append(name.split('/')[-1])
        
        
    def get_spectra(self,sel_meas):
        self.meas_attrs={}
        self.meas_data = []
        for meas in self.exp_meas:
            if sel_meas in meas:
                opendat = h5.File(meas,'r')
                gdata=[]
                for iset in opendat.keys():
                    if len(list(opendat.keys()))>1:
                        for jset in opendat[iset].keys():
                            gdata.append(opendat[iset][jset][:])
                            for attr in opendat[iset][jset].attrs.keys():
                                self.meas_attrs[attr] = opendat[iset][jset].attrs[attr]
                    else:
                        gdata.append(np.array(opendat[iset]))
                        try:
                            for attr in opendat[iset].attrs.keys():
                                self.meas_attrs[attr]= opendat[iset].attrs[attr]
                        except:
                            pass    
                self.meas_data.append(gdata)                   
                        
        return self.meas_attrs, self.meas_data[0]
            
                
                


            
            
            