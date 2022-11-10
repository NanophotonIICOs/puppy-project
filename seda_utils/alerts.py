import re
import streamlit as st
from processing import utils
def example_data_html(spectrometer):
    """
    Prepares string to show in manual, i.e. *.csv
    :param spectrometer: Str, name of the chosen spectrometer
    :return: Str
    """
    files = utils.load_example_files(spectrometer)
    text = files[0].read()
    files[0].seek(0)
    html = f'<div style="font-family: monospace"><p>{text}</p></div>'
    html = re.sub(r'\n', r'<br>', html)
    return html


