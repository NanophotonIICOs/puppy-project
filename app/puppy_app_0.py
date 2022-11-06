import streamlit as st
import pandas as pd
import numpy as np
import h5py as h5
import glob
from os import walk
import time
from matplotlib.gridspec import GridSpec
from nano_lab import experiments, afm_nsom
from mpl_toolkits.axes_grid1 import make_axes_locatable,ImageGrid, AxesGrid
import matplotlib as mpl
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotts as puppy
from PIL import Image

imicon = Image.open("images/diamond_2.png")


apptitle = "Puppy's Analysis"
st.set_page_config(page_title=apptitle, 
                    layout='wide', 
                    page_icon=imicon)

st.title("IICO Spectroscopy Experimental Data Analysis (Puppy's Master Thesis)")
st.markdown("Use the menu left to choice ")
st.write('<style>div.block-container{padding-top:0.75rem;}</style>', unsafe_allow_html=True)
st.sidebar.markdown("# Parameters")
st.write('<style>div.block-container{padding-top:-4rem;}</style>', unsafe_allow_html=True)
labs_list = ["nano-lab","spectro-lab-2"]
exp_list = ["nsom"]
select_lab = st.sidebar.selectbox('Select Laboratory',labs_list)
select_exp = st.sidebar.selectbox('Select Expriment',exp_list)

@st.cache
def get_list_samples():
    path='/media/labfiles/lab-exps'
    path = path+'/'+select_lab
    folder_samples=[]
    for folders in glob.glob(path+'/*'):
        folder_samples.append(folders.split(path)[-1].split('/')[-1])

    return folder_samples


with st.sidebar:
    sample=st.selectbox('Select sample',get_list_samples())
    exp = experiments(select_lab,select_exp,sample,False)
    noexp = st.selectbox("Select Measurement",exp.dframe['Name Dir'].tolist())
    try:
            step  = st.sidebar.number_input('Step (nm)',min_value=10,max_value=1000,step=10,key=int)
    except:
            step = 1
    plottypes = st.selectbox('Type of plots',['By sections','All 3D'])

count=0
for i in exp.dframe['Name Dir'].tolist():
    if i == noexp:
        break
    else:
        count+=1

try:
        exptoanalysis = afm_nsom(exp.data,count)
        afm    = exptoanalysis.afm
        lockin =  exptoanalysis.lockin
        multimeter =  exptoanalysis.multimeter
        #line = st.sidebar.slider('Line Profile', 0,17, 0)
        #st.pyplot(animate(line))
        aplot = puppy.plotts(afm,lockin,multimeter,step=step)
        if plottypes == 'All 3D':
            st.plotly_chart(aplot.plotting(),use_container_width=False)
        elif plottypes == 'By sections':
             exptype = st.sidebar.selectbox('Experiment',['afm','lockin','multimeter'])
             with st.container():
                    st.header(exptype.upper())
                    st.plotly_chart(aplot.plotall(exptype,step=step),use_container_width=True)
          
except IndexError or ValueError:
        with st.spinner("Loading..."):
            time.sleep(5)
    


# def select_exp(labNo,lab,system,nameofexp):
