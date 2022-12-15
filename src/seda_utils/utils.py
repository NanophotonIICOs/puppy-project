import base64
import plotly.express as px
import plotly.io as pio
import numpy as np
import streamlit as st
import pandas as pd
import peakutils
import glob
from nano_lab import experiments
from datetime import date
from datetime import datetime
import streamlit_nested_layout
from pathlib import Path
from pathlib import Path
import os
# iconpath1 = Path(__file__).parent / "seda_icons/logo_iico_azul.png"
# iconpath2 = Path(__file__).parent / "seda_icons/puppy_icon.png"
icons_path = os.path.abspath(os.path.dirname(__file__))
iconpathiico = os.path.join(icons_path, "seda_icons/logo_iico_azul.png")
iconpathpuppy = os.path.join(icons_path, "seda_icons/puppy_icon.png")


def trim_spectra(df):
    # trim raman shift range
    min_, max_ = int(float(df.index.min())), int(float(df.index.max())) + 1
    min_max = st.slider('Custom range', min_value=min_, max_value=max_, value=[min_, max_])
    min_rs, max_rs = min_max  #.split('__')
    min_rs, max_rs = float(min_rs), float(max_rs)
    mask = (min_rs <= df.index) & (df.index <= max_rs)
    return df[mask]


def show_iico_logo(width, padding, margin):
    with open(iconpathiico,'rb') as f:
        data = f.read()
    link = 'https://www.iico.uaslp.mx/#gsc.tab=0'
    padding_top, padding_right, padding_bottom, padding_left = padding
    margin_top, margin_right, margin_bottom, margin_left = margin
    
    bin_str = base64.b64encode(data).decode()
    html_code = f'''
                <a href="{link}" target = _blank>
                    <img src="data:image/png;base64,{bin_str}"
                    style="
                     margin: auto;
                     width: {width}%;
                     margin-top: {margin_top}px;
                     margin-right: {margin_right}px;
                     margin-bottom: {margin_bottom}px;
                     margin-left: {margin_left}%;
                     padding-top: {margin_top}px;
                     padding-right: {padding_right}px;
                     padding-bottom: {padding_bottom}px;
                     padding-left: {padding_left}%;
                     "/>
                 </a>
                '''
    return html_code


def show_seda_logo(width, padding, margin):
    padding_top, padding_right, padding_bottom, padding_left = padding
    margin_top, margin_right, margin_bottom, margin_left = margin
    
    with open(iconpathpuppy,'rb') as f:
        data = f.read()
    link = 'https://github.com/NanophotonIICOs/puppy-project'
    bin_str = base64.b64encode(data).decode()
    html_code = f'''
                <a href="{link}" target = _blank>
                <img src="data:image/png;base64,{bin_str}"
                style="
                     margin: auto;
                     width: {width}%;
                     margin-top: {margin_top}px;
                     margin-right: {margin_right}px;
                     margin-bottom: {margin_bottom}px;
                     margin-left: {margin_left}%;
                     padding-top: {margin_top}px;
                     padding-right: {padding_right}px;
                     padding-bottom: {padding_bottom}px;
                     padding-left: {padding_left}%;
                     "/>
                '''

    return html_code


def choose_template():
    """
    Choose default template from the list
    :return: Str, chosen template
    """
    template = st.selectbox(
        "Chart template",
        list(pio.templates), index=2, key='new')

    return template


def get_chart_vis_properties():
    palettes = {
        'qualitative': ['Alphabet', 'Antique', 'Bold', 'D3', 'Dark2', 'Dark24', 'G10', 'Light24', 'Pastel',
                        'Pastel1', 'Pastel2', 'Plotly', 'Prism', 'Safe', 'Set1', 'Set2', 'Set3', 'T10', 'Vivid',
                        ],
        'diverging': ['Armyrose', 'BrBG', 'Earth', 'Fall', 'Geyser', 'PRGn', 'PiYG', 'Picnic', 'Portland', 'PuOr',
                      'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral', 'Tealrose', 'Temps', 'Tropic', 'balance',
                      'curl', 'delta', 'oxy','Plotly3',
                      ],
        'sequential': ['Aggrnyl', 'Agsunset', 'Blackbody', 'Bluered', 'Blues', 'Blugrn', 'Bluyl', 'Brwnyl', 'BuGn',
                       'BuPu', 'Burg', 'Burgyl', 'Cividis', 'Darkmint', 'Electric', 'Emrld', 'GnBu', 'Greens', 'Greys',
                       'Hot', 'Inferno', 'Jet', 'Magenta', 'Magma', 'Mint', 'OrRd', 'Oranges', 'Oryel', 'Peach',
                       'Pinkyl', 'Plasma', 'Plotly3', 'PuBu', 'PuBuGn', 'PuRd', 'Purp', 'Purples', 'Purpor', 'Rainbow',
                       'RdBu', 'RdPu', 'Redor', 'Reds', 'Sunset', 'Sunsetdark', 'Teal', 'Tealgrn', 'Turbo', 'Viridis',
                       'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 'algae', 'amp', 'deep', 'dense', 'gray', 'haline', 'ice',
                       'matter', 'solar', 'speed', 'tempo', 'thermal', 'turbid',
                       ]
    }

    col1, col2, col3 = st.columns(3)

    with col1:
        palette_type = st.selectbox("Type of color palette", list(palettes.keys()), 0)
    with col2:
        palette = st.selectbox("Color palette", palettes[palette_type], index=0)
        if st.checkbox('Reversed', False):
            palette = palette + '_r'
    with col3:
        template = choose_template()

    palette_module = getattr(px.colors, palette_type)
    palette = getattr(palette_module, palette)

    return palette, template


def get_chart_vis_properties_vis():
    palettes = {
        'sequential': ['Plotly3','Aggrnyl', 'Agsunset', 'Blackbody', 'Bluered', 'Blues', 'Blugrn', 'Bluyl', 'Brwnyl', 'BuGn',
                       'BuPu', 'Burg', 'Burgyl', 'Cividis', 'Darkmint', 'Electric', 'Emrld', 'GnBu', 'Greens', 'Greys',
                       'Hot', 'Inferno', 'Jet', 'Magenta', 'Magma', 'Mint', 'OrRd', 'Oranges', 'Oryel', 'Peach',
                       'Pinkyl', 'Plasma', 'Plotly3', 'PuBu', 'PuBuGn', 'PuRd', 'Purp', 'Purples', 'Purpor', 'Rainbow',
                       'RdBu', 'RdPu', 'Redor', 'Reds', 'Sunset', 'Sunsetdark', 'Teal', 'Tealgrn', 'Turbo', 'Viridis',
                       'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd', 'algae', 'amp', 'deep', 'dense', 'gray', 'haline', 'ice',
                       'matter', 'solar', 'speed', 'tempo', 'thermal', 'turbid',
                       ],
        'qualitative': ['Alphabet', 'Antique', 'Bold', 'D3', 'Dark2', 'Dark24', 'G10', 'Light24', 'Pastel',
                        'Pastel1', 'Pastel2', 'Plotly', 'Prism', 'Safe', 'Set1', 'Set2', 'Set3', 'T10', 'Vivid',
                        ],
        'diverging': ['Armyrose', 'BrBG', 'Earth', 'Fall', 'Geyser', 'PRGn', 'PiYG', 'Picnic', 'Portland', 'PuOr',
                      'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral', 'Tealrose', 'Temps', 'Tropic', 'balance',
                      'curl', 'delta', 'oxy',
                      ],
        
    }
    print_widget_labels('Colors')
    palette_type = st.selectbox("Type of color palette", list(palettes.keys()) + ['custom'], 0)
    if palette_type == 'custom':
        palette = st.text_area('Hexadecimal colors', '#DB0457 #520185 #780A34 #49BD02 #B25AE8',
                               help='Type space separated hexadecimal codes')
        palette = palette.split()
    else:
        palette = st.selectbox("Color palette", palettes[palette_type], index=0)
        palette_module = getattr(px.colors, palette_type)
        palette = getattr(palette_module, palette)

    if st.checkbox('Reversed', True):
        palette = palette[::-1]


    print_widgets_separator(1)
    print_widget_labels('Template')
    template = choose_template()
    print_widgets_separator(1)

    return palette, template


def tick_step():
    print_widget_labels('Plot axis options')
    tsvalue = st.number_input('Axis tick Step',min_value=1,max_value=10,step=1,value=3)
    return int(tsvalue)

def tick_color():
    lscolor = ['black','white','red','blue','orange','pink','purple']
    tscolor  = st.color_picker('Ticks and plot lines color', '#0F06FF')
    return tscolor

def ticks():
    inner_cols = st.columns([1, 1])
    with inner_cols[0]:
        tscolor = st.color_picker('Color', '#0F06FF')
    with inner_cols[1]:
        tsfsize  = st.number_input('Font size',min_value=10,max_value=17,value=13,step=1)
    return tscolor, tsfsize


def fig_size():
    inner_cols = st.columns([1, 1])
    with inner_cols[0]:
        fig_width = st.number_input('Figure width:',min_value=400,max_value=900,value=400,step=50)
    with inner_cols[1]:
        fig_height = st.number_input('Figure height:',min_value=400,max_value=900,value=400,step=50)
    
    return fig_width, fig_width

def get_plot_description():
    print_widget_labels('Labels')
    xaxis = st.text_input('X axis name', r'x (nm)')
    yaxis = st.text_input('Y axis name', r'Intensity [au]')
    title = st.text_input('Title', r'')
    chart_titles = {'x': xaxis, 'y': yaxis, 'title': title}
    return chart_titles


def get_plot_description_pca():
    print_widget_labels('Labels')
    xaxis = st.text_input('X axis name', r'PC 1')
    yaxis = st.text_input('Y axis name', r'PC 2')
    title = st.text_input('Title', r'')
    chart_titles = {'x': xaxis, 'y': yaxis, 'title': title}
    return chart_titles

# def axis_step(value):
def print_widgets_separator(n=1, sidebar=False):
    """
    Prints customized separation line on sidebar
    """
    html = """<hr style="height:1px;
            border:none;color:#fff;
            background-color:#999;
            margin-top:5px;
            margin-bottom:10px"
            />"""

    for _ in range(n):
        if sidebar:
            st.sidebar.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown(html, unsafe_allow_html=True)


def print_widget_labels(widget_title, margin_top=5, margin_bottom=10):
    """
    Prints Widget label on the sidebar and lets adjust its margins easily
    :param widget_title: Str
    """
    st.markdown(
        f"""<p style="font-weight:500; margin-top:{margin_top}px;margin-bottom:{margin_bottom}px">{widget_title}</p>""",
        unsafe_allow_html=True)

    
def error_alert():
    st.warning("Error in file",icon="⚠️")
    
    

def get_exp(laboratory,spectra,sample,chosen_meas):
    class expfiles():pass
    expfiles = expfiles()
    exp = experiments(laboratory,spectra,sample)
    list_meas = exp.meas_list
    sel_meas =  counter_meas(chosen_meas,list_meas)
    if spectra == 'nsom':
        afm,nsom,multimeter = exp.afm_nsom_data(sel_meas)
        expfiles.afm = afm
        expfiles.nsom = nsom
        expfiles.multimeter = multimeter
    else:
        afm = exp.afm_nsom_data(sel_meas)
        expfiles.afm = afm

    attrs = exp.exps_attr(sel_meas)
    expfiles.list_meas = list_meas
    expfiles.attrs = attrs
    return expfiles    



def samples(select_lab):
    path='/media/labfiles/lab-exps'
    path = path+'/'+select_lab
    folder_samples=[]
    for folders in glob.glob(path+'/*'):
        folder_samples.append(folders.split(path)[-1].split('/')[-1])

    return folder_samples

def sel_samples(select_lab):
    path='/media/labfiles/lab-exps'
    path = path+'/'+select_lab
    folder_samples=[]
    for folders in glob.glob(path+'/*'):
        folder_samples.append(folders.split(path)[-1].split('/')[-1])

    return folder_samples


#couter to select correct measure, from selectbox
def counter_meas(chosen_meas,list_meas):
    count=0
    for i in list_meas:
        if i == chosen_meas:
            break
        else:
            count+=1
    return count

def get_spectra(laboratory,spectra,sample,choosen_meas):
    exp = experiments(laboratory,spectra,sample,False)
    list_meass = exp.meas_list
    sel_meas = counter_meas(choosen_meas,list_meas)
    if spectra =='nsom':
        afm,nsom,multimeter = exp.afm_nsom_data(sel_meas)
        return afm,nsom,multimeter
    else:
        afm = exp.afm_nsom_data(sel_meas)
        return afm
        
@st.cache
def get_attrs(laboratory,spectra,sample,choosen_meas):
    exp = experiments(laboratory,spectra,sample,False)
    list_meas = exp.meas_list
    sel_meas = counter_meas(choosen_meas,list_meas)
    attrs = exp.exps_attr(sel_meas)
    return attrs


def pline(data_attrs):
    """
    Move profile line aorund sptecra with a x-pixel (matrix element) value
    :param normalized:
    :return: Int or Float
    """
    
    if data_attrs:
        yi = int(data_attrs['Inicio Y'])
        yf = int(data_attrs['fin Y '])
        step = int(data_attrs['paso'])
        yrange = np.arange(yi,yf/step).tolist()
        yfn = int(yf/step)
        vdefault  = int((yfn)/2)
        ypix =  st.slider('y-pix', min_value=yi,
                        max_value=yfn,step=1,value=vdefault)
        return ypix
    else :
        ypix=1
        return ypix
        #error_alert()
    

@st.cache
def get_data_spectra(exp,sel_meas):
    meas = exp.exp_meas
    if meas:
        attrs, data = exp.get_spectra(sel_meas)
        if data[0].ndim>2:
            #print(data[0].shape)
            afm  = data[0][:,:,0]
            nsom = data[0][:,:,1]
            return afm, nsom, attrs
        else:
            afm = data[0]
            return afm, attrs

    
    
def data_properties(attrs):
    dframe =  pd.DataFrame.from_dict([attrs]).T
    dframe.columns=["Values"]
    # dframe.columns.names=['Parameters']
    dframe.index.names=['Parameters']
    #st.dataframe(dframe,use_container_width=True)
    st.table(dframe)
    
def save_data(data):
    data_type = st.radio(
    "Choose spectra type ",
    ('afm', 'nsom'))
    now = datetime.now()
    date = now.strftime("%Y-%d-%b-%H:%M:%S")
    fname = data_type+'-'+date+'.csv'


    if data[0].ndim>2:
            afm  = data[0][:,:,0]
            nsom = data[0][:,:,1]
    else:
        afm = data[0]
        nsom = None
    
    if data_type == 'afm':
        sel_data = pd.DataFrame(afm).to_csv(index=False).encode('utf-8')
    if data_type == 'nsom':
        sel_data = pd.DataFrame(nsom).to_csv(index=False).encode('utf-8')

    
    st.download_button( label="Download data as CSV",
    data=sel_data,
    file_name=fname,
    mime='text/csv',
)
    

    
            
        
        
    