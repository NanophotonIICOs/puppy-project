import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, mpld3
import requests, os
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
import math
mpl.rcParams.update(mpl.rcParamsDefault)
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plotdata(afm,lockin,multimeter,**kwargs):
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'surface'}, {'type': 'surface'},{'type': 'surface'}]])
    # Generate data
    nx = afm.shape[0]
    ny = afm.shape[1]
    x = np.arange(0, nx, 1)
    y = np.arange(0, ny, 1)
    fig.add_trace(
        go.Surface(x=x, y=y, z=afm, colorscale='Plotly3',showscale=False),
        row=1, col=1)
    fig.update_traces(contours_z=dict(show=True, usecolormap=True,highlightcolor="limegreen", project_z=True))

    fig.add_trace(
        go.Surface(x=x, y=y, z=lockin, colorscale='Plotly3',showscale=False),
        row=1, col=2)
    fig.update_traces(contours_z=dict(show=True, usecolormap=True,highlightcolor="limegreen", project_z=True))

    fig.add_trace(
        go.Surface(x=x, y=y, z=multimeter, colorscale='Plotly3',showscale=False),
        row=1, col=3)
    fig.update_traces(contours_z=dict(show=True, usecolormap=True,highlightcolor="limegreen", project_z=True))

    fig.update_layout(
        title_text='AFM, Lockin, Multimeter data results',autosize=True,
        height=500,
        width=900,
        #margin=dict(l=50, r=50, b=30, t=35)
    )
    return fig

apptitle = "Puppy's Analysis"
st.set_page_config(page_title=apptitle, page_icon=":blue_heart:")
st.title("Image analysis from spectro lab (Puppy's Master Thesis)")
st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# st.markdown("""
#  * Use the menu at left to select data and set plot parameters
#  * Your plots will appear below
# """)
st.markdown("""
  <style>
    .css-znku1x.e16nr0p33 {
      margin-top: -1000px;
    }
  </style>
""", unsafe_allow_html=True)
st.sidebar.markdown("# Parameters")
labs_list = ["nano-lab","spectro-lab-2"]
exp_list = ["nsom"]
select_lab = st.sidebar.selectbox('Select Laboratory',labs_list)
select_exp = st.sidebar.selectbox('Select Expriment',exp_list)

def get_list_samples():
    path='/media/labfiles/lab-exps'
    path = path+'/'+select_lab
    folder_samples=[]
    for folders in glob.glob(path+'/*'):
        folder_samples.append(folders.split(path)[-1])
    return folder_samples


with st.sidebar:
    sample=st.selectbox('Select sample',get_list_samples())
    exp = experiments(select_lab,select_exp,sample,False)
    noexp = st.selectbox("Select Measurement",exp.dframe['Name Dir'].tolist())

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
        st.plotly_chart(plotdata(afm,lockin,multimeter))
        








except IndexError or ValueError:
        with st.spinner("Loading..."):
            time.sleep(5)
    


# def select_exp(labNo,lab,system,nameofexp):
