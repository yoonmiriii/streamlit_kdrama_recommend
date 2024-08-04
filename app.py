import streamlit as st
from streamlit_option_menu import option_menu 
import streamlit.components.v1 as html
from  PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import io
import pickle

from home import run_home 
from eda import run_eda
from ml import run_ml


def main():

    menu = ['홈화면', '드라마 통계', '드라마 추천받기']

    st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """,
    unsafe_allow_html=True
)

    with st.sidebar:
        choice = option_menu('Category', ['홈화면', '드라마 통계 ', '드라마 추천받기'],
                icons=['house', 'film', 'star'],
                menu_icon = "", default_index=0,
                styles={
                # default_index = 처음에 보여줄 페이지 인덱스 번호
                        "container": {"padding": "5!important", "background-color": "#0080fa"},  #카테고리 색상
                        "icon": {"color": "orange", "font-size": "25px"}, 
                        "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px",
                                     "color": "#000000", "--hover-color": "##e0e0e0"},  
                        "nav-link-selected": {"background-color": "#ffffff"},
    } # css 설정
    )

    if choice == menu[0] :
        run_home()

    elif choice == menu[1] :
        run_eda()

    # elif choice == menu[2] :
    #     run_ml()
    
    

if __name__ == '__main__':
    main()




