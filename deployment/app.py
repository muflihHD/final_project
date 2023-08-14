import streamlit as st
import eda
import prediction
import model

st.set_page_config(
    page_title='Plant Analysis',
    layout='centered',
    initial_sidebar_state= 'auto'
    )

navbar = st.sidebar.selectbox('#### Page:',('Analysis','Prediction', 'Model'))

if navbar =='Analysis':
    eda.run()
elif navbar == 'Prediction':
    prediction.run()
elif navbar == 'Model':
    model.run()