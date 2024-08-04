import joblib
import pickle
import streamlit as st
import numpy as np
import os

import pickle
import streamlit as st

def run_ml():
    def get_recommendations(name):
        # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값을 얻기
        idx = drama[drama['Name'] == name].index[0]

        # 코사인 유사도 매트릭스 (cosine_sim) 에서 idx 에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
        sim_scores = list(enumerate(cosine_sim[idx]))

        # 코사인 유사도 기준으로 내림차순 정렬
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
        sim_scores = sim_scores[1:11]

        # 추천 영화 목록 10개의 인덱스 정보 추출
        drama_indices = [i[0] for i in sim_scores]

        # 인덱스 정보를 통해 영화 제목 추출
        recommended_names = [drama['Name'].iloc[i] for i in drama_indices]
        return recommended_names

    # 데이터 로드
    drama = pickle.load(open('drama.pickle', 'rb'))
    cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

    st.set_page_config(layout='wide')
    st.header('드라마 추천')

    drama_list = drama['Name'].values
    selected_name = st.selectbox('선택하세요', drama_list)

    if st.button('추천'):
        recommended_names = get_recommendations(selected_name)
        
        # 추천 결과를 5열의 레이아웃으로 출력
        num_cols = 5
        cols = st.columns(num_cols)
        for i, col in enumerate(cols):
            if i < len(recommended_names):
                col.write(recommended_names[i])
