import base64
import plotly.express as px
import plotly.io as pio
import numpy as np
import streamlit as st
import pandas as pd
import peakutils
import glob
from nano_lab import experiments

def trim_spectra(df):
    # trim raman shift range
    min_, max_ = int(float(df.index.min())), int(float(df.index.max())) + 1
    min_max = st.slider('Custom range', min_value=min_, max_value=max_, value=[min_, max_])
    min_rs, max_rs = min_max  #.split('__')
    min_rs, max_rs = float(min_rs), float(max_rs)
    mask = (min_rs <= df.index) & (df.index <= max_rs)
    return df[mask]


@st.cache
def show_iico_logo(width, padding, margin):
    with open('seda_icons/iico.png', 'rb') as f:
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


@st.cache
def show_seda_logo(width, padding, margin):
    padding_top, padding_right, padding_bottom, padding_left = padding
    margin_top, margin_right, margin_bottom, margin_left = margin
    
    link = ' '
    
    with open('seda_icons/diamond_2.png', 'rb') as f:
        data = f.read()
    
    bin_str = base64.b64encode(data).decode()
    html_code = f'''
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
        list(pio.templates), index=6, key='new')

    return template


def get_chart_vis_properties():
    palettes = {
        'qualitative': ['Alphabet', 'Antique', 'Bold', 'D3', 'Dark2', 'Dark24', 'G10', 'Light24', 'Pastel',
                        'Pastel1', 'Pastel2', 'Plotly', 'Prism', 'Safe', 'Set1', 'Set2', 'Set3', 'T10', 'Vivid',
                        ],
        'diverging': ['Armyrose', 'BrBG', 'Earth', 'Fall', 'Geyser', 'PRGn', 'PiYG', 'Picnic', 'Portland', 'PuOr',
                      'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral', 'Tealrose', 'Temps', 'Tropic', 'balance',
                      'curl', 'delta', 'oxy',
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
        'qualitative': ['Alphabet', 'Antique', 'Bold', 'D3', 'Dark2', 'Dark24', 'G10', 'Light24', 'Pastel',
                        'Pastel1', 'Pastel2', 'Plotly', 'Prism', 'Safe', 'Set1', 'Set2', 'Set3', 'T10', 'Vivid',
                        ],
        'diverging': ['Armyrose', 'BrBG', 'Earth', 'Fall', 'Geyser', 'PRGn', 'PiYG', 'Picnic', 'Portland', 'PuOr',
                      'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral', 'Tealrose', 'Temps', 'Tropic', 'balance',
                      'curl', 'delta', 'oxy',
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

    if st.checkbox('Reversed', False):
        palette = palette[::-1]

    print_widgets_separator(1)
    print_widget_labels('Template')
    template = choose_template()
    print_widgets_separator(1)

    return palette, template

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


@st.cache
def samples(select_lab):
    path='/media/labfiles/lab-exps'
    path = path+'/'+select_lab
    folder_samples=[]
    for folders in glob.glob(path+'/*'):
        folder_samples.append(folders.split(path)[-1].split('/')[-1])

    return folder_samples


#couter to select correct measure, from selectbox
def counter_measure(chosen_measure,list_measure):
    count=0
    for i in list_measure:
        if i == chosen_measure:
            break
        else:
            count+=1
    return count


@st.cache
def get_spectra(laboratory,spectra,sample,choosen_measure):
    exp = experiments(laboratory,spectra,sample,False)
    data = exp.data
    dframe = exp.dframe
    list_measures = dframe['Name Dir'].tolist()
    sel_measure = counter_measure(choosen_measure,list_measures)
    afm,nsom,multimeter = exp.afm_nsom_data(sel_measure)
    return afm,nsom,multimeter

@st.cache
def get_attrs(laboratory,spectra,sample,choosen_measure):
    exp = experiments(laboratory,spectra,sample,False)
    dframe = exp.dframe
    list_measures = dframe['Name Dir'].tolist()
    sel_measure = counter_measure(choosen_measure,list_measures)
    attrs = exp.exps_attr(sel_measure)
    return attrs

def pline(data_attrs):
    """
    Move profile line aorund sptecra with a x-pixel (matrix element) value
    :param normalized:
    :return: Int or Float
    """
    xi = int(data_attrs['Inicio X'])
    xf = int(data_attrs['fin X '])
    step = int(data_attrs['paso'])
    xrange = np.arange(xi,xf/step).tolist()
    xpix =  st.slider('x-pix', 0.0,1.0,2.0)
    xpix = int(xpix)
    return xpix
    
    
