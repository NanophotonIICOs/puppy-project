import streamlit as st
from seda import utils


def main_page():
    sersitivis_logo = utils.show_sersitivis_logo(width=65, padding=[0, 6, 20, 25], margin=[0, 0, 30, 0])
    st.markdown(sersitivis_logo, unsafe_allow_html=True)
    
    cols = st.columns((1, 6, 1))
    with cols[1]:
        st.header("SEDA IICO")
        st.subheader("Spectroscopy Experimental Data Analysis")

    cols = st.columns((3, 3, 1))
    with cols[1]:
        st.subheader("By")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
    
    iico_logo = utils.show_logo(width=65, padding=[0, 6, 20, 25], margin=[0, 0, 30, 0])
    st.markdown(iico_logo, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    st.markdown("")
