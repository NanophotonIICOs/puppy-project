import numpy as np
import pandas as pd
import peakutils
import plotly.express as px
import streamlit as st


from seda_utils import  sidebar,utils,charts
from seda_visual import visual_options as vis_opt
from seda_visual import seda_plots  as splots
from nano_lab import get_data



# def run_time_exp(laboratory):
#     st.sidebar.button('check real-time experiment')