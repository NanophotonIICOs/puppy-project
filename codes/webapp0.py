import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests, os
import h5py as h5
import glob
from os import walk
from matplotlib.gridspec import GridSpec
from IPython.display import display, clear_output
from labexp import experiments
from mpl_toolkits.axes_grid1 import make_axes_locatable,ImageGrid, AxesGrid
from matplotlib.gridspec import GridSpec
plt.style.use('/media/labfiles/lab-codes/plot-styles/plotstyle.mplstyle')

apptitle = "Puppy's Analysis"

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

st.title("Image analysis from spectro lab (Puppy's Master Tesis)")

st.markdown("""
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
""")

st.sidebar.markdown("## Select experiment")q

# def select_exp(labNo,lab,system,nameofexp):
