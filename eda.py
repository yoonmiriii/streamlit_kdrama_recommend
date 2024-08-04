import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from collections import Counter
from googletrans import Translator

# 번역기 클래스
class Google_Translator:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, lang='ko'):
        try:
            return self.translator.translate(text, dest=lang).text
        except Exception as e:
            st.write(f"번역 오류: {e}")
            return text

    def translate_df(self, df, lang='ko'):
        df_translated = df.copy()
        for column in df.columns:
            if df[column].dtype == 'object':  # 텍스트 열만 번역
                df_translated[column + '_translated'] = df[column].apply(lambda x: self.translate_text(x, lang) if pd.notnull(x) else x)
        return df_translated

    def translate_list(self, text_list, lang='ko'):
        return [self.translate_text(text, lang) for text in text_list]


# print(st.__version__)


def run_eda() : 

    df = pd.read_csv('./data/kdrama.csv')
    st.dataframe(df.head())

    # 데이터프레임의 기본 정보 표시
    st.write("DataFrame Information:")
    st.write(df.info())

    # 번역 기능
    translator = Google_Translator()

    # 버튼 클릭 시 전체 데이터 번역
    if st.button('모든 텍스트 번역하기'):
        df_translated = translator.translate_df(df, 'ko')
        st.write('모든 텍스트 번역 결과:')
        st.dataframe(df_translated.head())

    if st.button('그래프 보기', help='클릭해주세요.', use_container_width=True) :
        fig1 = plt.figure()   # figure 객체 생성해줘야 오류 메세지 안 생김
        sb.countplot(data=df, x='Year of release', color='green')
        plt.xlabel('Year')
        plt.ylabel('Number of Dramas')
        plt.title('연도별 방영된 드라마 수')
        plt.xticks(rotation=45)
        plt.grid(axis='y')  # y축에 그리드 추가
        st.pyplot(fig1)

        st.text('')
        st.text('')

    if st.button('방송사별 방영된 드라마 수') :
                
        search_words = ['Netflix', 'Wavve', 'ENA', 'tvN', 'jTBC', 'OCN', 'SBS', 'KBS2', 'MBC', 'Daum Kakao TV', 'Olleh TV', 'Disney+', 'Channel A', 'TV Chosun', 'Naver TV Cast', 'MBN']
        counts = {}
        for word in search_words:
            counts[word] = df[df['Original Network'].str.contains(word, case=False, na=False)].shape[0]
        # 딕셔너리를 값(counts)으로 내림차순 정렬
        counts_sorted = dict(sorted(counts.items(), key=lambda item: item[1], reverse=False))

        # 결과를 가로 막대 그래프로 출력
        fig2 = plt.figure(figsize=(12, 8))
        plt.barh(list(counts_sorted.keys()), list(counts_sorted.values()), color='skyblue')
        plt.xlabel('Number of Dramas')
        plt.ylabel('Network')
        plt.title('방송사별 방영된 드라마 수')
        plt.grid(axis='x')  # x축에 그리드 추가
        st.pyplot(fig2)

    if st.button('장르별 드라마 수 비율') :
        genre_counts = Counter()
        for i in df['Genre']:
            genres = i.split(', ')
            for genre in genres:
                genre_counts[genre.strip()] += 1
        # 상위 15개 장르 추출
        top_genres = genre_counts.most_common(15)
        labels = [genre[0] for genre in top_genres]
        sizes = [genre[1] for genre in top_genres]

        # 파이차트 그리기
        fig3 = plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=30, wedgeprops={'width':0.7})
        plt.axis('equal')  # 원 모양으로 조정
        plt.title('장르별 드라마 수 비율')
        st.pyplot(fig3)

    if st.button('에피소드 수') :

        # 에피소드 수와 시청 시간 시각화
        fig4 = plt.figure(figsize=(10, 6))
        sb.scatterplot(x='Number of Episodes', y='Duration', data=df)
        plt.title('Number of Episodes vs. Duration')
        plt.xlabel('Number of Episodes')
        plt.ylabel('Duration (minutes)')
        plt.grid(True)
        st.pyplot(fig4)

    if st.button('감독별 평점') : 
        # ' ' 데이터 제외하고 감독별 평균 평점 계산
        director_ratings = df[df['Director'] != ''].groupby('Director')['Rating'].mean().sort_values(ascending=False).head(10)

        # 시각화
        fig5 = plt.figure(figsize=(12, 8))
        director_ratings.plot(kind='bar')
        plt.title('Top 10 Directors by Average Rating')
        plt.xlabel('Director')
        plt.ylabel('Average Rating')
        plt.xticks(rotation=45)
        st.pyplot(fig5)

    if st.button('배우 출연작품 수') : 
        cast_counts = df['Cast'].str.split(',').explode().str.strip().value_counts()

        # 상위 10명 캐스트만 추출
        top_cast = cast_counts.head(50)

        # 시각화
        fig6 = plt.figure(figsize=(12, 20))
        top_cast.plot(kind='barh')
        plt.title('Top 10 Cast Members by Number of Dramas')
        plt.xlabel('Number of Dramas')
        plt.ylabel('Cast Member')
        plt.gca().invert_yaxis()  # 순서 뒤집기 (가장 많은 것이 위에 오도록)
        st.pyplot(fig6)

    if st.button('시청등급') : 
        R_labels = df['Content Rating'].value_counts()

        # ' ' 데이터 제외하기
        R_labels = R_labels[R_labels.index != ' ']

        # 시청 등급별 개수와 라벨 리스트 생성
        labels = R_labels.index.tolist()  # 시청 등급
        sizes = R_labels.values.tolist()  # 개수

        # 파이차트 그리기
        fig7 = plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=30, wedgeprops={'width':0.7})
        plt.axis('equal')  # 원 모양으로 조정
        plt.title('시청 등급 비율')
        st.pyplot(fig7)

    st.subheader('장르별 드라마')
    column_list = ['선택해주세요','Action',
 'Adventure',
 'Business',
 'Comedy',
 'Crime',
 'Drama',
 'Family',
 'Fantasy',
 'Food',
 'Friendship',
 'Historical',
 'Horror',
 'Law',
 'Life',
 'Medical',
 'Melodrama',
 'Military',
 'Music',
 'Mystery',
 'Political',
 'Psychological',
 'Romance',
 'School',
 'Sci-Fi',
 'Sitcom',
 'Sports',
 'Supernatural',
 'Thriller',
 'Youth']
    translated_column_list = translator.translate_list(column_list, 'ko')


    my_choice = st.selectbox('장르를 선택하세요', column_list)
            
    if my_choice == column_list[0] : 
        st.text('')

    else:
        # 'Genre' 열에서 선택한 장르가 포함된 드라마 필터링
        genre_drama = df[df['Genre'].str.contains(my_choice, case=False, na=False)]

        # 필터링된 드라마 제목을 리스트로 출력
        if not genre_drama.empty:
            st.write(f'{my_choice} 장르에 속하는 드라마:')
            st.write(genre_drama['Name'].tolist())  # 'Name' 열에서 제목을 추출
        else:
            st.write(f'선택한 장르({my_choice})에 해당하는 드라마가 없습니다.')


        








# # Streamlit 애플리케이션 실행
# if __name__ == "__main__":
#     run_eda()