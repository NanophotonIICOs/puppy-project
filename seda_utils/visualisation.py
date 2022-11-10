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

    chosen_sample = sidebar.choose_sample(laboratory)
    spectra = sidebar.nano_lab_choose_spectra_type()
    chosen_meas = sidebar.choose_measure(laboratory,spectra,chosen_sample)
    #data
    try:
        exp = utils.get_exp(laboratory, spectra, chosen_sample, chosen_meas)
        afm = exp.afm
        nsom = exp.nsom
        data_attrs = exp.attrs
    except:
        exp = utils.get_exp(laboratory, spectra, chosen_sample, chosen_meas)
        afm = exp.afm
        data_attrs = exp.attrs
        with st.expander('Error File'):
            st.write("This file corresponds to older version, therefore doesn't have nsom experiments")
            

    
    # sidebar separating line
    utils.print_widgets_separator(1, sidebar=True)
    
    if exp:
        st.spinner('Uploading data in progress')
    
        col_left, col_right = st.columns([5, 2])
        
        
        with col_right:
            normalized = False
            
    #         # # Plot settings
            plot_settings = st.expander("Plot settings", expanded=True)
            
    #         # # Choose plot colors and templates
            with plot_settings:
                tsvalue = utils.tick_step()
                plots_color, template = utils.get_chart_vis_properties_vis()
                
            range_expander_name = 'Line profile pixel'
            range_expander = st.expander(range_expander_name, expanded=True)
             
            with range_expander:
               ypix = utils.pline(data_attrs)
            
            
        
        # Data plotting
            
        with col_left:
            if spectra == 'nsom':
                with st.expander('AFM',expanded=True):
                    figs=splots.fig_3d_2d_layout(afm,template,data_attrs,ypix,plots_color,tick_step=tsvalue)
                    st.plotly_chart(figs,use_container_width=True,)
                    
                with st.expander('NSOM',expanded=True):
                    figs=splots.fig_3d_2d_layout(nsom,template,data_attrs,ypix,plots_color,tick_step=tsvalue)
                    st.plotly_chart(figs,use_container_width=True)
            elif spectra == 'afm':
                try:
                    with st.expander('AFM',expanded=True):
                        figs=splots.fig_3d_2d_layout(afm,template,data_attrs,ypix,plots_color,tick_step=tsvalue)
                        st.plotly_chart(figs,use_container_width=True,)
                except:
                    pass
                    