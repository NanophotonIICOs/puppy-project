import os
import sentry_sdk
import streamlit as st
from seda_utils import (authors, main_page, real_time_experiment, sidebar,
                        visualisation)

if os.path.isfile(".streamlit/secrets.toml"):
    if 'sentry_url' in st.secrets:
        sentry_sdk.init(
            st.secrets['sentry_url'],
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=0.001,
        )
    else:
        print('sentry not running')
else:
    print('Ok')

def main():
    """
    Main is responsible for the visualisation of everything connected with streamlit.
    It is the web application itself.
    """
    # # Radiobuttons in one row
    # st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    # Sets sidebar's header and logo
    sidebar.sidebar_head()
    list_options =['Main Page', 'Nano Lab']
    analysis_type = st.sidebar.selectbox("Choose Laboratory",list_options,disabled=False )

    if analysis_type == 'Main Page':
        main_page.main_page()
    if analysis_type == 'Nano Lab':
        laboratory = "nano-lab"
        options = st.sidebar.selectbox('Choose an option',["Visualization data","Real-time experiment"])
        if options =="Visualization data":
            visualisation.visualisation(laboratory)
        elif options == "Real-time experiment":
            real_time_experiment.run_time_exp(laboratory)


    #     visualisation.visualisation()
    # elif analysis_type == 'PCA':
    #     pca.main()
    # elif analysis_type == 'EF':
    #     enhancement_factor.main()
    # elif analysis_type == 'RSD':
    #     rsd.main()
    authors.show_developers()


if __name__ == '__main__':
    # try:
    #     import streamlit_analytics
    #
    #     credential_file = 'tmp_credentials.json'
    #     if not os.path.exists(credential_file):
    #         with open(credential_file, 'w') as infile:
    #             infile.write(st.secrets['firebase_credentials'])
    #         print('credentials written')
    #
    #     collection = datetime.date.today().strftime("%Y-%m")
    #     with streamlit_analytics.track(firestore_key_file=credential_file,
    #                                    firestore_collection_name=collection,
    #                                    # verbose=True
    #                                    ):
    #         main()
    # except KeyError:
    #     main()

    main()

    #print("puppy ")  