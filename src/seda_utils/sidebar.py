import streamlit as st
from seda_utils import utils
from constants import LABELS
import os
from nano_lab import experiments
from PIL import Image

icons_path = os.path.abspath(os.path.dirname(__file__))
iconpathpuppy = os.path.join(icons_path, "seda_icons/puppy_icon.png")

imicon = Image.open(iconpathpuppy)

def sidebar_head():
    """
    Sets Page title, page icon, layout, initial_sidebar_state
    Sets position of radiobuttons (in a row or one beneath another)
    Shows logo in the sidebar
    """
    st.set_page_config(
        page_title="SEDA IICO",
        page_icon=imicon,
        layout="wide",
        initial_sidebar_state="auto"
    )
    st.set_option('deprecation.showfileUploaderEncoding', False)
    #puppy logo
    html_code = utils.show_seda_logo(100, [0, 0, 0, 0], margin=[0, 0, 0, 0])
    st.sidebar.markdown(html_code, unsafe_allow_html=True)
    st.sidebar.markdown('')
    st.sidebar.markdown('')


def print_widget_labels(widget_title, margin_top=5, margin_bottom=10):
    """
    Prints Widget label on the sidebar and lets adjust its margins easily
    :param widget_title: Str
    """
    st.sidebar.markdown(
        f"""<p style="font-weight:500; margin-top:{margin_top}px;margin-bottom:{margin_bottom}px">{widget_title}</p>""",
        unsafe_allow_html=True)


def choose_sample(laboratory):
    samples = utils.samples(laboratory)
    s_samples = st.sidebar.selectbox(
        "Sample",
        samples,
        index=3
        )
    return s_samples


def choose_spectra_type():
    spectra_types = ['nsom','afm']
    spectrometer = st.sidebar.selectbox(
        "Spectra type",
        spectra_types,
        # format_func=LABELS.get,
        )
    return spectrometer

def show_experiments(exp):
    meas = exp.exp_meas
    if meas:
        list_meas = [i.split('/')[-1] for i in exp.exp_meas[::-1]]
        expmeas = st.sidebar.selectbox(
                "Experiments",
                list_meas,
                index=0)
        return expmeas
