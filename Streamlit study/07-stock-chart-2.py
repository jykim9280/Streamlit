import streamlit as st
import FinanceDataReader as fdr
import datetime
import time

st.title('종목 차트 검색')

with st.sidebar: #사이드바 및 하단 컴포넌트 정의
    date = st.date_input(
        "조회 시작일을 선택해 주세요",
        datetime.datetime(2022, 1, 1)
    )

    code = st.text_input(
        '종목코드', 
        value='',
        placeholder='종목코드를 입력해 주세요'
    )

if code and date:  # code랑 date가 둘다 None이 아닐 경우
    try:
        df = fdr.DataReader(code, date)
        if not df.empty:
            data = df.sort_index(ascending=True).loc[:, 'Close']  # DataFrame으로 날짜순 정렬, 날짜랑 종가 입력
        else:
            st.write("해당 기간에 데이터가 존재하지 않습니다.")
    except Exception as e:
        st.write(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")

    tab1, tab2 = st.tabs(['차트', '데이터'])

    with tab1:    
        st.line_chart(data)

    with tab2:
        st.dataframe(df.sort_index(ascending=False))

    with st.expander('컬럼 설명'):
        st.markdown('''
        - Open: 시가
        - High: 고가
        - Low: 저가
        - Close: 종가
        - Adj Close: 수정 종가
        - Volumn: 거래량
        ''')
