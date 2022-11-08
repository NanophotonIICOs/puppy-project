import pandas as pd
import peakutils
import plotly.express as px
import streamlit as st

# noinspection PyUnresolvedReferences
# import str_slider
# from processing import utils, save_read
from seda_utils import  sidebar,utils,charts
# import utils as utils
from seda_visual import visual_options as vis_opt
from seda_visual import seda_plots  as splots

def visualisation(laboratory):
    #

    spectra = sidebar.nano_lab_choose_spectra_type()
    choose_sample = sidebar.choose_sample(laboratory)
    choose_measure = sidebar.choose_measure(laboratory,spectra,choose_sample)
    #data
    afm,nsom,multimeter = utils.get_spectra(laboratory,spectra,choose_sample,choose_measure)
    data_attrs = utils.get_attrs(laboratory,spectra,choose_sample,choose_measure)
    
    # sidebar separating line
    utils.print_widgets_separator(1, sidebar=True)
    
    if choose_measure:
        st.spinner('Uploading data in progress')
    
        col_left, col_right = st.columns([5, 2])
        
        
        with col_right:
            normalized = False
            
    #         # # Plot settings
            plot_settings = st.expander("Plot settings", expanded=False)
            
    #         # # Choose plot colors and templates
            with plot_settings:
                plots_color, template = utils.get_chart_vis_properties_vis()
                
            range_expander_name = 'Line profile pixel'
            range_expander = st.expander(range_expander_name, expanded=False)
             
            with range_expander:
               xpix = utils.pline(data_attrs)
            
            
        
        # Data plotting
            
        with col_left:
            with st.expander('AFM'):
                figs=splots.fig_3d_2d_layout(afm,template,xpix)
                st.plotly_chart(figs,use_container_width=True)
                
            with st.expander('NSOM'):
                figs=splots.fig_3d_2d_layout(nsom,template,xpix)
                st.plotly_chart(figs,use_container_width=True)
    