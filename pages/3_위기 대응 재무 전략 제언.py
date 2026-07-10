import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 데이터 캐시 로드 함수
@st.cache_data
def load_page_two_data():
    df = pd.read_csv("cleaned_startup_total.csv")
    df['연도'] = df['연도'].astype(str) if '연도' in df.columns else df['연度'].astype(str)
    return df

try:
    df = load_page_two_data()
except Exception as e:
    st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 2. 페이지 상단 제목 및 기획 배경
st.title("🛡️ 거시경제 위기 대응 재무 전략 제언")
st.caption("Page 2: Data-Driven Financial Strategy Guide")
st.markdown("""
> **"위기 상황에서 경영자는 어떤 재무 전략을 짜야 하는가?"**

본 페이지는 감이나 유행이 아닌, **KOSIS 10개년 데이터 시뮬레이션**을 통해 이 질문에 답합니다. 
가장 강력한 거시경제 충격기였던 **2020년(팬데믹 쇼크)**과 **2021년(유동성 과열기)**의 산업별 전년 대비 창업기업수 증감률을 분석하여, 
각 산업군에 가장 적합한 **회계적 방어기제와 자본 배분 전략**을 제언합니다.
""")
st.markdown("---")

# 3. 데이터 연산 (산업 대분류별 위기 시기 평균 변동률 계산)
# 전체 데이터의 연도별, 대분류별 창업기업수 합계 계산
agg_df = df.groupby(['연도', '대분류'])['창업기업수'].sum().reset_index()
agg_df = agg_df.sort_values(by=['대분류', '연도']).reset_index(drop=True)

# 대분류별 증감률 계산
agg_df['증감률(%)'] = 0.0
major_list = agg_df['대분류'].unique()

for major in major_list:
    idx = agg_df[agg_df['대분류'] == major].index
    for i in range(1, len(idx)):
        prev_val = agg_df.loc[idx[i-1], '창업기업수']
        curr_val = agg_df.loc[idx[i], '창업기업수']
        if prev_val > 0:
            change = ((curr_val - prev_val) / prev_val) * 100
            agg_df.loc[idx[i], '증감률(%)'] = round(change, 2)

# 4. 사용자의 산업 대분류 선택
st.subheader("🏭 분석할 산업군 선택")
selected_major = st.selectbox("🎯 경영 전략을 확인할 산업 대분류를 선택하세요.", major_list)

# 선택된 산업군의 2020, 2021년 데이터 추출
major_df = agg_df[agg_df['대분류'] == selected_major]
try:
    shock_2020 = major_df[major_df['연도'] == '2020']['증감률(%)'].values[0]
    shock_2021 = major_df[major_df['연도'] == '2021']['증감률(%)'].values[0]
except IndexError:
    shock_2020, shock_2021 = 0.0, 0.0

# 5. 매트릭스 시각화
col1, col2 = st.columns(2)
with col1:
    st.metric(label=f"[{selected_major}] 2020년 팬데믹 변동률", value=f"{shock_2020}%")
with col2:
    st.metric(label=f"[{selected_major}] 2021년 유동성 과열기 변동률", value=f"{shock_2021}%")

st.markdown("---")

# =========================================================================
# 6. 알고리즘 기반 데이터 기반 재무 전략 매트릭스 도출
# =========================================================================
st.subheader("📝 맞춤형 회계·경영 전략 보고서")

# 분류 기준 설정
is_sensitive = shock_2020 <= -10 or shock_2021 <= -10
is_growth = shock_2020 >= 10 or shock_2021 >= 10

if is_sensitive:
    st.error(f"🚨 **{selected_major}** : 외부 충격에 크게 흔들리는 **'경기 민감형 위험지대'** 분석 결과")
    
    # 4대 재무 전략 제언
    strat_col1, strat_col2 = st.columns(2)
    with strat_col1:
        st.markdown("""
        ### 💵 1. 현금성 자산 (Cash Buffer)
        - **진단:** 외부 충격 시 수요가 급감하여 매출 채권 회수가 지연될 리스크가 매우 높습니다.
        - **전략:** 고정비의 최소 6개월 치에 달하는 **비상 운전자본(Cash Cushion)**을 상시 확보해야 합니다. 현금성 자산의 비중을 자산 총액의 20% 이상으로 유지하는 것을 권장합니다.
        """)
        st.markdown("""
        ### 📊 2. 비용 구조 (Cost Structure)
        - **진단:** 매출 감소 시 높은 고정비는 손익분기점(BEP)을 급격히 상승시켜 대규모 적자를 유발합니다.
        - **전략:** 설비 직접 구매 대신 리스나 아웃소싱을 활용하여 **고정비를 변동비화(Variable Costing)**해야 합니다. 임차료, 인건비 등 고정성 경비를 즉시 슬림화할 수 있는 매뉴얼을 구축하세요.
        """)
    with strat_col2:
        st.markdown("""
        ### 📈 3. 투자 및 ROI
        - **진단:** 불확실성이 높은 시기의 무리한 설비 투자는 자본 유연성을 완전히 고갈시킵니다.
        - **전략:** 신규 투자를 전면 재검토하거나 동결하고, **보수적인 회수기간법(Payback Period)**을 적용하여 1년 이내에 현금화가 가능한 효율화 중심의 소규모 투자만 집행해야 합니다.
        """)
        st.markdown("""
        ### 🏦 4. 자본 조달 (Financing)
        - **진단:** 위기 발발 후에는 신용 등급 하락 및 금리 인상으로 자금 조달 창구가 막힙니다.
        - **전략:** 경기 호황기에 미리 **장기 저리 고정금리 대출**이나 한도대출(마이너스 통장)을 확보해 두어야 합니다. 국책과제나 정부 정책자금 등 타인자본 조달 채널을 다각화하세요.
        """)

elif is_growth:
    st.info(f"🚀 **{selected_major}** : 위기를 성장의 발판으로 삼는 **'역발상 기회 포착형'** 분석 결과")
    
    strat_col1, strat_col2 = st.columns(2)
    with strat_col1:
        st.markdown("""
        ### 💵 1. 현금성 자산 (Cash Buffer)
        - **진단:** 위기 상황에서 신규 수요가 폭발하므로 현금을 쥐고 있기보다는 빠르게 시장을 선점해야 합니다.
        - **전략:** 과도한 현금 보유는 기회비용을 발생시킵니다. 운영에 필요한 최소 현금만 유지하고, 나머지는 **공격적인 운전자본(재고자산 확보, 공격적 마케팅 비용)으로 신속히 전환**해야 합니다.
        """)
        st.markdown("""
        ### 📊 2. 비용 구조 (Cost Structure)
        - **진단:** 급증하는 수요에 대응하기 위해 인프라와 공급망의 빠른 확장이 필요합니다.
        - **전략:** 규모의 경제를 달성하기 위해 **고정비 투자를 아끼지 않아야 할 시기**입니다. 핵심 인재 채용 및 인프라 고도화에 자본을 집중하여 경쟁사와의 격차를 벌리세요.
        """)
    with strat_col2:
        st.markdown("""
        ### 📈 3. 투자 및 ROI
        - **진단:** 시장의 판도가 바뀌는 대격변기는 장기 성장의 핵심 적기입니다.
        - **전략:** 단기 손익에 연연하기보다 **장기적 투자수익률(ROI) 및 LTV(고객생애가치)** 관점에서 대규모 투자를 집행해야 합니다. 위기로 무너진 경쟁 업체의 자산이나 인력을 인수(M&A)하는 전략도 유효합니다.
        """)
        st.markdown("""
        ### 🏦 4. 자본 조달 (Financing)
        - **진단:** 투자 유치 및 지분 금융(Equity Financing)을 조달하기에 가장 유리한 환경이 조성됩니다.
        - **전략:** 고금리 타인자본(대출)보다는 스타트업 붐이나 정책적 우대 혜택을 활용하여 **벤처캐피탈(VC) 투자 유치나 증자**를 통한 자본 확충을 최우선으로 고려해야 합니다.
        """)

else:
    st.success(f"🛡️ **{selected_major}** : 대외 위기에도 끄떡없는 **'저변동 안전지대'** 분석 결과")
    
    strat_col1, strat_col2 = st.columns(2)
    with strat_col1:
        st.markdown("""
        ### 💵 1. 현금성 자산 (Cash Buffer)
        - **진단:** 급격한 유동성 위기나 급격한 성장 변동이 적은 안정적인 구조입니다.
        - **전략:** 예측 가능한 현금 흐름을 바탕으로 현금 보유고를 적정 수준(안정 자본)으로 유효하게 관리하며, 남는 유동성은 안정적인 단기 금융상품(MMF 등)으로 운용하는 자본 효율성이 필요합니다.
        """)
        st.markdown("""
        ### 📊 2. 비용 구조 (Cost Structure)
        - **진단:** 경기 변동에 큰 영향을 받지 않으므로 무리하게 비용을 줄일 필요가 없습니다.
        - **전략:** 현재의 효율적인 손익분기점(BEP) 구조를 유지하되, 내부 프로세스 자동화나 디지털 전환(DX)을 통해 **장기적인 한계비용을 낮추는 내부 내실 다지기**에 집중하는 것이 좋습니다.
        """)
    with strat_col2:
        st.markdown("""
        ### 📈 3. 투자 및 ROI
        - **진단:** 급격한 확장은 오히려 고정비 부담으로 돌아와 안정을 해칠 수 있습니다.
        - **전략:** 신규 시장 개척보다는 기존 핵심 비즈니스의 락인(Lock-in) 효과를 높이는 투자가 적절합니다. 철저한 **정밀 가치평가(Valuation)**를 거친 자본 예산(Capital Budgeting) 내에서만 점진적 투자를 집행하세요.
        """)
        st.markdown("""
        ### 🏦 4. 자본 조달 (Financing)
        - **진단:** 꾸준한 현금 창출력 덕분에 금융권에서 가장 선호하는 신용도가 높은 상태입니다.
        - **전략:** 외부 지분 투자(증자)를 통해 주주 지분을 희석하기보다, 신용도를 바탕으로 한 **시중은행의 저리 대출이나 영업활동현금흐름 자체를 재투자 자원**으로 활용하는 내부 유보금 전략이 유리합니다.
        """)

st.markdown("---")

# =========================================================================
# 7. 전체 산업 대분류 비교 차트 시각화
# =========================================================================
st.markdown("##### 📊 전체 산업 대분류별 위기 상황 변동성 비교")

# 시각화를 위한 피벗 변환
chart_df = agg_df[agg_df['연도'].isin(['2020', '2021'])].copy()

fig2 = px.bar(
    chart_df, 
    x='대분류', 
    y='증감률(%)', 
    color='연도',
    barmode='group',
    title="2020년 vs 2021년 산업별 충격 반응도 비교",
    template='plotly_white',
    color_discrete_map={'2020': '#ef4444', '2021': '#3b82f6'}
)

fig2.update_layout(
    dragmode='pan',
    xaxis=dict(fixedrange=False, title="산업 대분류"),
    yaxis=dict(fixedrange=False, title="증감률 (%)")
)

st.plotly_chart(
    fig2, 
    width='stretch', 
    theme="streamlit",
    config={'displayModeBar': False, 'scrollZoom': True}
)

st.markdown("---")
st.caption("Data Source: KOSIS 법인·개인 합산 업종별 창업기업 통계(2016-2025) | Page 2")
