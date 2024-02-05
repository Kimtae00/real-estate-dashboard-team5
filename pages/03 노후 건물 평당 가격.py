import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import plotly.subplots as sp
import plotly.graph_objects as go



selected_house_types = st.multiselect(
    '건물 유형 선택',
    ['아파트', '단독다가구', '오피스텔', '연립다세대'],
    default=['아파트']
  )  # 기본 선택값 설정

data = pd.concat([pd.read_csv(f'data/{house_type}.csv') for house_type in selected_house_types])



# 사용자 입력을 통한 데이터 선택
#selected_SGG = st.selectbox('구를 선택해주세요:', data2['SGG_NM'].unique())
#selected_index = st.selectbox('동을 선택해주세요:', data2.loc[data2['SGG_NM'] == selected_SGG, 'BJDONG_NM'].unique())
# 선택한 구와 동을 사이드바에서 선택

selected_SGG = st.sidebar.selectbox('구 선택', data['SGG_NM'].unique())
selected_index = st.sidebar.selectbox(
    '동 선택', data.loc[data['SGG_NM'] == selected_SGG, 'BJDONG_NM'].unique()
)

# 선택한 HOUSE_TYPE에 대한 데이터 필터링 및 각 HOUSE_TYPE에 대한 막대 그래프 생성
fig = go.Figure()

for house_type in selected_house_types:
    # 선택한 HOUSE_TYPE에 대한 데이터 필터링
    filtered_data = data[(data['SGG_NM'] == selected_SGG) & (data['BJDONG_NM'] == selected_index) & (data['HOUSE_TYPE'] == house_type)]

    # PRICE_PER의 평균 계산
    average_price_per = filtered_data['PRICE_PER'].mean()

    # 막대 그래프에 추가
    fig.add_trace(go.Bar(x=[f"{house_type} 평균 가격"], y=[average_price_per], name=house_type))

# 그래프 레이아웃 설정
fig.update_layout(
    title=f'{", ".join(selected_house_types)}의 {selected_SGG}, {selected_index} 지역 1평당 평균 가격',
    xaxis_title='House Type',
    yaxis_title='1평당 평균 가격'
)

# 차트를 화면에 표시
st.plotly_chart(fig)

option = st.selectbox(
    '건물 유형 선택',('아파트', '단독다가구', '오피스텔', '연립다세대')
    )

data2 = pd.read_csv(f'data/{option}.csv')

# PyDeck 차트 표시
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=37.5665,  # 서울시 중심 좌표
        longitude=126.9780,
        zoom=10,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ColumnLayer',
            data=data2,
            get_position=['CENTER_LONG', 'CENTER_LATI'],
            get_elevation='PRICE_PER',
            elevation_scale=0.5,  # 높이 스케일 조정
            radius=100,  # 막대의 반지름
            get_fill_color=[255, 165, 0, 100],  # 막대 색상 설정
            pickable=True,
            auto_highlight=True,
        ),
        pdk.Layer(
            'ColumnLayer',
            data=data2[data2['BJDONG_NM'] == selected_index],
            get_position=['CENTER_LONG', 'CENTER_LATI'],
            get_elevation='PRICE_PER',
            elevation_scale=0.5,  # 높이 스케일 조정
            radius=200,  # 막대의 반지름
            get_fill_color=[0, 0, 255, 200],  # 막대 색상 설정
            pickable=True,
            auto_highlight=True,
        ),
    ],
))


# 고른 자료 표시 
st.write(data2[data2['BJDONG_NM'] == selected_index])




