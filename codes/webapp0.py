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



plt.style.use('/media/labfiles/lab-codes/plot-styles/plotstyle.mplstyle')

apptitle = "Puppy's Analysis"

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

st.title("Image analysis from spectro lab (Puppy's Master Tesis)")

st.markdown("""
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
""")

st.sidebar.markdown("## Select experiment")

labs_list = ["Lab. Nano","Lab. Spectro II Cryostat 1","Lab. Spectro II Cryostat 2", "Lab. Ellipsometry"]


exp_list = ["RAS","AFM"]

#-- Set time by GPS or event
select_lab = st.sidebar.selectbox('Select Laboratory',
                                    labs_list)

sample=st.sidebar.text_input('Input sample name')

@st.cache(ttl=3600, max_entries=1)   #-- Magic command to cache data
def get_exp(select_lab,sample):
    if select_lab=="Lab. Nano":
        lab='nano'
        types='nsom'
        nolab=1
    exp = experiments(1,lab,types,sample,False)
    return [exp.dframe,exp]

st.table(get_exp(select_lab,sample)[0])

noexp=st.sidebar.text_input("Select No. Dir: ")
afm = get_exp(select_lab,sample)[1].data[int(noexp)][0][:,:,0].T

with _lock:
    fig = plt.figure(figsize=(5, 5))
    gs = GridSpec(1, 2, figure=fig,wspace=0.25,hspace=0.21,width_ratios=[1,1])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 =fig.add_subplot(gs[0, 1])
    ax1.set_title("AFM")
    ax1.imshow(afm[:,1:],cmap='cool',aspect='auto',interpolation='gaussian')

    st.pyplot(fig)



    #fig1 = cropped.plot()
    


# def select_exp(labNo,lab,system,nameofexp):
