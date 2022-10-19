import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests, os
import h5py as h5
import glob
from os import walk
from matplotlib.gridspec import GridSpec
from labexp import experiments
from mpl_toolkits.axes_grid1 import make_axes_locatable,ImageGrid, AxesGrid
from matplotlib.gridspec import GridSpec
import matplotlib as mpl
plt.style.use('/media/labfiles/lab-codes/puppy-project/src/plotstyle.mplstyle')

mpl.use("agg")

##############################################################################
# Workaround for the limited multi-threading support in matplotlib.
# Per the docs, we will avoid using `matplotlib.pyplot` for figures:
# https://matplotlib.org/3.3.2/faq/howto_faq.html#how-to-use-matplotlib-in-a-web-application-server.
# Moreover, we will guard all operations on the figure instances by the
# class-level lock in the Agg backend.
##############################################################################
from matplotlib.backends.backend_agg import RendererAgg
_lock = RendererAgg.lock

apptitle = "Puppy's Analysis"

st.set_page_config(page_title=apptitle, page_icon=":blue_heart:")
st.title("Image analysis from spectro lab (Puppy's Master Thesis)")
# st.markdown("""
#  * Use the menu at left to select data and set plot parameters
#  * Your plots will appear below
# """)

st.sidebar.markdown("# Parameters")

labs_list = ["nano-lab","spectro-lab-2"]

exp_list = ["afm","nsom","ras","pr"]

select_lab = st.sidebar.selectbox('Select Laboratory',labs_list)
select_exp = st.sidebar.selectbox('Select Expriment',exp_list)

def get_list_samples():
    path='/media/labfiles/lab-exps'
    path = path+'/'+select_lab
    folder_samples=[]
    for folders in glob.glob(path+'/*'):
        folder_samples.append(folders.split(path)[-1])
    return folder_samples

sample=st.sidebar.selectbox('Select sample',get_list_samples())

#noexp=st.sidebar.text_input("Select No. Dir: ",value=1)

exp = experiments(select_lab,select_exp,sample,False)
noexp = st.sidebar.selectbox("Select Measurement",exp.dframe['Name Dir'].tolist())

count=0
for i in exp.dframe['Name Dir'].tolist():
    if i == noexp:
        break
    else:
        count+=1

# dframe=exp.dframe
# st.table(dframe)
afm = exp.data[count][0][:,:,0].T
line = st.sidebar.slider('pixel', 0,5, 1)
ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
    background: rgb(1 1 1 / 0%); } </style>''', unsafe_allow_html = True)


Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
    background-color: rgb(14, 38, 74); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)

    
Slider_Number = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div > div
                                { color: rgb(14, 38, 74); } </style>''', unsafe_allow_html = True)
    

col = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div {{
    background: linear-gradient(to right, rgb(1, 183, 158) 0%, 
                                rgb(1, 183, 158) {line}%, 
                                rgba(151, 166, 195, 0.25) {line}%, 
                                rgba(151, 166, 195, 0.25) 100%); }} </style>'''

ColorSlider = st.markdown(col, unsafe_allow_html = True) 

with _lock:
    fig = plt.figure(figsize=(5, 2))
    fig.patch.set_facecolor('none')
    gs = GridSpec(1, 2, figure=fig,wspace=0.3,hspace=0.3,width_ratios=[1,1])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 =fig.add_subplot(gs[0, 1])
    ax1.imshow(afm[:,1:],origin='lower',cmap='cool',aspect='auto',interpolation='gaussian')
    ax1.plot([0,43],[line,line],'r')
    ax2.plot(afm[line,1:],'o-r',ms=4,lw=1,mfc='none')
    ax2.patch.set_facecolor('none')

    st.pyplot(fig,clear_figure=True)



    #fig1 = cropped.plot()
    


# def select_exp(labNo,lab,system,nameofexp):
