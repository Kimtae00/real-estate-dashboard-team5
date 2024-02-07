import pandas as pd
import streamlit as st
import re
from crawling import get_news_data
import plotly.express as px
import time

st.set_page_config(layout="wide")

# HTML 태그 제거 함수
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# 데이터 불러오기
data_danlist = pd.read_csv('data/단독다가구.csv')
data_yeonlist = pd.read_csv('data/연립다세대.csv')

# 연립다세대, 단독다가구에 해당하는 데이터 병합하기
combined_data = pd.concat([data_danlist, data_yeonlist])

# 데이터 로드 및 필터링
data = pd.read_csv("data/Seoul_data.csv")

# 데이터 준비
current_year = pd.to_datetime('today').year
data['Building Age'] = current_year - data['BUILD_YEAR']
data['Age Category'] = data['Building Age'].apply(lambda x: '20년 이상' if x >= 20 else '20년 미만')

unique_combin = data.drop_duplicates(subset=['SGG_CD', 'BJDONG_CD','BLDG_NM','BUILD_YEAR'],keep='first').copy()
unique_combin = unique_combin.reset_index(drop=True)

# 20년 이상, 구>동 건물개수 상위 10개
district_age_data = unique_combin.groupby(['SGG_NM', 'BJDONG_NM','Age Category']).size().reset_index(name='Count')

# '20년 이상' 필터링 및 내림차순 정렬
dong_10 = district_age_data[district_age_data['Age Category'] == '20년 이상'].nlargest(10, 'Count')

# 'Name' 열 추가
dong_10['Name'] = dong_10['SGG_NM'] + ' ' + dong_10['BJDONG_NM']

# 시각화
fig = px.bar(
    dong_10,  # 수정된 데이터프레임 사용
    x="Name", 
    y="Count", 
    color='Name', 
    labels={'Name': '지역', 'Count': '노후 건물수', 'SGG_NM' : '지역'},
    text="Count",
    title='노후 건물 개수 상위 10개 지역',
    width=1100,
    height=500
)

#x축 정렬 설정
fig.update_xaxes(categoryorder='total descending')
st.plotly_chart(fig)
st.markdown("---")

# 20년 이상된 건물의 거래만 고려
old_transactions = data[data['Age Category'] == '20년 이상']

# 'DISTRICT' 열 생성
old_transactions['DISTRICT'] = old_transactions['SGG_NM'] + ' ' + old_transactions['BJDONG_NM']

selected_house_types = ['연립다세대', '단독다가구']
filtered_data = old_transactions[old_transactions['HOUSE_TYPE'].isin(selected_house_types)]
building_counts_by_district = filtered_data.groupby('DISTRICT').size().reset_index(name='TRANSACTION_COUNT')
top10_districts = building_counts_by_district.nlargest(10, 'TRANSACTION_COUNT')

# 시각화
fig = px.bar(
    top10_districts,
    x='DISTRICT',
    y='TRANSACTION_COUNT',
    text='TRANSACTION_COUNT',
    title='노후 건물 거래량 상위 10개 지역',
    labels={'DISTRICT': '지역', 'TRANSACTION_COUNT': '노후 건물 거래량'},
    color='DISTRICT',
    width=1100,
    height=500
)
st.plotly_chart(fig)
st.markdown("---")

# 화곡동을 재개발에서 제외한 이유
st.markdown('#### 강서구 화곡동을 재개발 부지에서 제외한 이유')
st.write('부동산 투기로 인한 가격 상승으로 인해 **산출가격 기준 초과**로 재개발 부지 선정에서 제외')

# 화곡동에 해당하는 데이터만 필터링
filtered_data = combined_data[combined_data['BJDONG_NM'] == '화곡동']


# 필드명 한글로 변경
filtered_data = filtered_data.rename(columns={
    'HOUSE_TYPE': '건물유형',
    'PRICE_PER': '평균 평당가격',
    'BJDONG_NM': '법정동 명',
    'SGG_NM': '구 명',
    'CENTER_LONG': '경도',
    'CENTER_LATI': '위도'
})

# 평균 평당가격을 반올림하여 정수로 변환하고 '만원' 단위 붙이기
filtered_data['평균 평당가격'] = filtered_data['평균 평당가격'].round(0).astype(int).astype(str) + "만원"

# 테이블로 표시
st.table(filtered_data)

with st.expander("관련 뉴스 보기"):
    st.write(
        '<iframe width="100%" height="900px" src="https://v.daum.net/v/20230423114233323" frameborder="1" allowfullscreen></iframe>',
        unsafe_allow_html=True
    )

# 다이어그램
st.markdown('#### 재개발로 선정된 지역')
st.image('images/재개발 선정 지역.png', caption='재개발 선정 지역', width=700)

# # 버튼을 사용하여 뉴스 정보 로드
# if st.sidebar.button("재개발 관련 뉴스 정보 가져오기"):
#     st.markdown('##### 재개발로 선정된 지역의 재개발 관련 뉴스 정보를 가져옵니다.')
#     queries = ['관악구 신림동 재개발', '강북구 수유동 재개발', '관악구 봉천동 재개발', '양천구 신월동 재개발', '강북구 미아동 재개발']
#     for query in queries:
#         news = get_news_data(query)
#         if news:
#             st.subheader(f"{query} 관련 뉴스")
#             for item in news:
#                 title = remove_html_tags(item['title'])
#                 link = item['link']
#                 st.markdown(f"[{title}]({link})")
#             st.markdown('---')
            
            
# Initialize the progress bar and status text
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

# Your existing web crawling code with modifications for the progress bar
if st.sidebar.button("재개발 관련 뉴스 정보 가져오기"):
    queries = ['관악구 신림동 재개발', '강북구 수유동 재개발', '관악구 봉천동 재개발', '양천구 신월동 재개발', '강북구 미아동 재개발']
    
    total_queries = len(queries)
    for i, query in enumerate(queries):
        news = get_news_data(query)
        if news:
            st.subheader(f"{query} 관련 뉴스")
            for item in news:
                title = remove_html_tags(item['title'])
                link = item['link']
                st.markdown(f"[{title}]({link})")
            st.markdown('---')
        
        # Update progress
        progress = int((i + 1) / total_queries * 100)
        status_text.text(f"{progress}% Complete")
        progress_bar.progress(progress)
        time.sleep(0.05)  # Optional delay to see progress bar updating

    # Clear the progress bar after completion
    progress_bar.empty()

