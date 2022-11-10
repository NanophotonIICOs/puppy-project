import streamlit as st
from seda_utils import utils
from constants import LABELS

from nano_lab import experiments

def sidebar_head():
    """
    Sets Page title, page icon, layout, initial_sidebar_state
    Sets position of radiobuttons (in a row or one beneath another)
    Shows logo in the sidebar
    """
    st.set_page_config(
        page_title="SEDA IICO",
        page_icon="seda_icons/puppy_icon.png",
        layout="wide",
        initial_sidebar_state="auto"
    )

    st.set_option('deprecation.showfileUploaderEncoding', False)

    # SERSitivis logo
    html_code = utils.show_seda_logo(80, [0, 0, 0, 0], margin=[0, 0, 0, 15])
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
        #format_func=LABELS.get,
        index=3
        )
    return s_samples


def nano_lab_choose_spectra_type():
    spectra_types = ['nsom','afm']
    spectrometer = st.sidebar.selectbox(
        "Spectra type",
        spectra_types,
        # format_func=LABELS.get,
        )
    return spectrometer

def choose_measure(laboratory,experiment,sample):
    try:
        exp = experiments(laboratory,experiment,sample)
        list_meas = exp.meas_list[::-1]
        measures = st.sidebar.selectbox(
            "Experiment Measure",
            list_meas,
            index=0)
        return  measures
    except (AttributeError,IndexError):
        utils.error_alert()
    