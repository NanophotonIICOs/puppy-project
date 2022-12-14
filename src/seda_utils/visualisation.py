import pandas as pd
import peakutils
import plotly.express as px
import streamlit as st
from seda_utils import  sidebar,utils,charts
# import utils as utils
from seda_visual import visual_options as vis_opt
from seda_visual import seda_plots  as splots
from nano_lab import get_data

def visualisation(laboratory):
    chosen_sample = sidebar.choose_sample(laboratory)
    spectra = sidebar.choose_spectra_type()
    exp = get_data(laboratory, spectra, chosen_sample)
    exp_meas = sidebar.show_experiments(exp)
    data = utils.get_data_spectra(exp, exp_meas)

    
    # sidebar separating line
    col_left, col_right = st.columns([5, 2])
    if exp_meas:
        if spectra == 'nsom':
            afm = data[0]
            nsom = data[1]
            attrs = data[2]
        elif spectra == 'afm':
            afm = data[0]
            attrs = data[1]       
        
        
        with col_right:
            normalized = False

            plot_settings = st.expander("Plot settings", expanded=True)
            
             # Choose plot colors and templates
            with plot_settings:
                tsvalue = utils.tick_step()
                tscolor, tsfsize = utils.ticks()
                fig_width, fig_height = utils.fig_size()
                plots_color, template = utils.get_chart_vis_properties_vis()
                
            range_expander_name = 'Line profile pixel'
            range_expander = st.expander(range_expander_name, expanded=True)
             
            with range_expander:
               ypix = utils.pline(attrs)
            
            data_properties =  st.expander("Experimental Measurement Properties", expanded=False)
            with data_properties:
                utils.data_properties(attrs)
                
        # Data plottin
        
        
        
        with col_left:
            st.header('Plots')
            if spectra == 'nsom':
                with st.expander('AFM',expanded=True):
                    figs=splots.fig_3d_2d_layout(afm,
                                                 template,
                                                 attrs,
                                                 ypix,
                                                 plots_color,
                                                 tick_step=tsvalue,
                                                 tick_color=tscolor,
                                                 fig_width=fig_width,
                                                 fig_height=fig_height,
                                                 fsize=tsfsize)
                    st.plotly_chart(figs,use_container_width=True,)
                    
                    
                with st.expander('NSOM',expanded=True):
                    figs=splots.fig_3d_2d_layout(nsom,
                                                 template,
                                                 attrs,
                                                 ypix,
                                                 plots_color,
                                                 tick_step=tsvalue,
                                                 tick_color=tscolor,
                                                 fig_width=fig_width,
                                                 fig_height=fig_height,
                                                 fsize=tsfsize)
                    st.plotly_chart(figs,use_container_width=True)
                    
                st.header('Export Data')
                
                with st.expander("Save data"):
                    utils.save_data(data)
                
                
            elif spectra == 'afm':
                try:
                    with st.expander('AFM',expanded=True):
                        figs=splots.fig_3d_2d_layout(afm,
                                                     template,
                                                     attrs,
                                                     ypix,
                                                     plots_color,
                                                     tick_step=tsvalue,
                                                     tick_color=tscolor,
                                                     fsize=tsfsize)
                        st.plotly_chart(figs,use_container_width=True,)
                except:
                    pass
            
            
    else:
        with col_left:
            st.info('These spectra have not available', icon="ℹ️")


