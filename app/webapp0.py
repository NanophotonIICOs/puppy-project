import streamlit as st
import pandas as pd
import numpy as np
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
        specs=[[{'type': 'surface'}, {'type': 'surface'},{'type': 'surface'}]],
        horizontal_spacing = 0.02,
         subplot_titles=["AFM","LockIn","Multimeter"],
         shared_xaxes=True,
         shared_yaxes=True,
         column_widths=[400,400,400],
         row_heights=[300],)

    if 'step' in kwargs:
        step = kwargs.get('step')
    else: 
        step =1
    # Generate data
    nx = afm.shape[0]
    ny = afm.shape[1]
    x = np.arange(0, nx, 1)
    y = np.arange(0, ny, 1)
    xt =np.arange(x[0],x[-1],5)
    xtl = xt*step

    exp2plots = [afm,lockin,multimeter]
    for i,expriment in enumerate(exp2plots):
        fig.add_trace(
            go.Surface( z=expriment, colorscale='Plotly3',showscale=False,reversescale=True),row=1, col=i+1)
        #fig.update_traces(contours_x=dict(show=True, usecolormap=True, project_x=True))
        #fig.update_traces(contours_y=dict(show=True, usecolormap=True, project_y=True))

    fig.update_layout(
        template="plotly_dark",
        width=1300,
        font=dict(
            family="Computer Modern Roman,serif",
            color='black',
            size=13,
        ),
         margin=dict(l=5, r=5, b=10, t=20),
         scene=dict(
    xaxis=dict(title = 'x (nm)',tickmode='array',ticktext=xtl,tickvals=xt,),
    yaxis=dict(title = 'y (nm)',tickmode='array',ticktext=xtl,tickvals=xt,)),
    scene2=dict(
    xaxis=dict(title = 'x (nm)',tickmode='array',ticktext=xtl,tickvals=xt,),
    yaxis=dict(title = 'y (nm)',tickmode='array',ticktext=xtl,tickvals=xt,)),
    scene3=dict(
    xaxis=dict(title = 'x (nm)',tickmode='array',ticktext=xtl,tickvals=xt,),
    yaxis=dict(title = 'y (nm)',tickmode='array',ticktext=xtl,tickvals=xt,)),
    )
  
    return fig

apptitle = "Puppy's Analysis"
st.set_page_config(page_title=apptitle, page_icon=":blue_heart:")
st.title("Image analysis from spectro lab (Puppy's Master Thesis)")
st.write('<style>div.block-container{padding-top:0.75rem;}</style>', unsafe_allow_html=True)
st.sidebar.markdown("# Parameters")
st.write('<style>div.block-container{padding-top:-4rem;}</style>', unsafe_allow_html=True)
labs_list = ["nano-lab","spectro-lab-2"]
exp_list = ["nsom"]
select_lab = st.sidebar.selectbox('Select Laboratory',labs_list)
select_exp = st.sidebar.selectbox('Select Expriment',exp_list)
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
        try:
            step  = st.sidebar.number_input('Step (nm)',min_value=10,max_value=1000,step=10,key=int)
        except:
            step = 1
        refresh_server=st.sidebar.button('Update current experiment')

        st.plotly_chart(plotdata(afm,lockin,multimeter,step=step))

        
        
except IndexError or ValueError:
        with st.spinner("Loading..."):
            time.sleep(5)
    


# def select_exp(labNo,lab,system,nameofexp):
