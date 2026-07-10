import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 캐시 로드 함수
@st.cache_data
def load_page_one_data():
    df = pd.read_csv("cleaned_startup_total.csv")
    df['연도'] = df['연도'].astype(str) if '연도' in df.columns else df['연度'].astype(str)
    return df

try:
    df = load_page_one_data()
except Exception as e:
    st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 2. 페이지 상단 제목 및 레이아웃
st.title("📈 업종별 창업 기업 수 추이 및 외부 충격 영향 진단")
st.markdown("""
특정 업종을 선택하여 대외적 거시경제 충격(2020년 코로나 팬데믹, 2021년 자산 과열기)이 발생했을 때 
해당 산업이 받은 영향을 진단하고 10개년간의 창업 기업 수 변화 추이를 관찰합니다.
""")
st.markdown("---")

# 3. 메인 페이지 내 업종 필터 기능 구현 (사이드바에서 이동)
st.subheader("🔍 분석 대상 업종 선택")
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    major_categories = df['대분류'].unique()
    selected_major = st.selectbox("🎯 산업 대분류", major_categories)

# 대분류 선택에 따른 소분류 필터링
sub_df = df[df['대분류'] == selected_major]

with filter_col2:
    selected_minor = st.selectbox("🔎 세부 업종 (소분류)", sub_df['소분류'].unique())

# =========================================================================
# 4. [수정] 데이터 타입 강제 변환 및 연도별 정렬 순서 보정 프로세스
# =========================================================================
# 소분류 필터링 후, 연도를 정수형(int)으로 정렬한 뒤 다시 시각화용 문자열(str)로 변환합니다.
industry_df = sub_df[sub_df['소분류'] == selected_minor].copy()

# 연도 컬럼을 숫자로 바꾸어 정확하게 오름차순 정렬 (2016 -> 2025)
industry_df['연도_형변환'] = industry_df['연도'].astype(int)
industry_df = industry_df.sort_values(by='연도_형변환').reset_index(drop=True)
industry_df['연도'] = industry_df['연도_형변환'].astype(str)

pct_changes = [0.0]
for i in range(1, len(industry_df)):
    prev_val = industry_df.loc[i-1, '창업기업수']
    curr_val = industry_df.loc[i, '창업기업수']
    if prev_val > 0:
        change = ((curr_val - prev_val) / prev_val) * 100
        pct_changes.append(round(change, 2))
    else:
        pct_changes.append(0.0)

industry_df['증감률(%)'] = pct_changes
# 5. 핵심 재무 지표 (KPI) 스코어보드
col1, col2 = st.columns(2)

try:
    shock_2020 = industry_df[industry_df['연도'] == '2020']['증감률(%)'].values[0]
    shock_2021 = industry_df[industry_df['연도'] == '2021']['증감률(%)'].values[0]
except IndexError:
    shock_2020, shock_2021 = 0.0, 0.0

with col1:
    st.metric(label="2020년 팬데믹 쇼크기 변동률", value=f"{shock_2020}%", delta="코로나19 발발", delta_color="off")
with col2:
    st.metric(label="2021년 유동성 과열기 변동률", value=f"{shock_2021}%", delta="자산시장 급변", delta_color="off")

st.markdown("---")


# =========================================================================
# 6. [위치 이동 및 간결화] 알고리즘 기반 경영·회계적 리스크 분석 보고서
# =========================================================================
st.markdown(f"### 🔍 **{selected_minor}** 업종의 거시경제 위기 저항력 진단 결과")

# [1단계] 고변동성 경기 민감 업종 (충격 폭이 마이너스로 매우 크거나 극심한 타격을 입은 경우)
if shock_2020 <= -15 or shock_2021 <= -15:
    st.error("🚨 [결과 핵심] 외부 충격에 취약한 고변동성 경기 민감 업종")
    st.markdown(f"""
    - **리스크 진단:** 대격변기 당시 급격한 하락세(2020년 **{shock_2020}%** / 2021년 **{shock_2021}%**)를 기록하여 외부 환경에 민감하게 동요합니다.
    - **재무 제언:** 고정비 비율을 최소화하고, 최소 3~6개월을 버틸 수 있는 **비상 운전자본(Cash Buffer)**을 두텁게 확보해 자본 지속가능성을 강화해야 합니다.
    """)

# [2단계] 위기 극복 및 기회 포착형 업종 (위기 상황 속에서 오히려 창업이 늘어난 경우)
elif shock_2020 >= 10 or shock_2021 >= 10:
    st.info("🚀 [결과 핵심] 외부 충격을 기회로 삼은 역발상 성장형 업종")
    st.markdown(f"""
    - **리스크 진단:** 대격변기(2020년 **{shock_2020}%** / 2021년 **{shock_2021}%**) 속에서 오히려 플러스를 기록하거나 빠른 반등에 성공하며 시장의 새로운 수요를 흡수했습니다.
    - **재무 제언:** 위기가 곧 기회가 된 업종입니다. 단기적인 생존보다는 시장 점유율 확대를 위한 공격적인 투자 및 신규 서비스 고도화(ROI 중심 마케팅) 전략이 유효합니다.
    """)

# [3단계] 저변동성 불황 저항형 업종 (위 1, 2단계에 해당하지 않고 안정적인 기조를 유지한 경우)
else:
    st.success("🛡️ [결과 핵심] 대외 위기에도 견고한 저변동성 불황 저항형 업종")
    st.markdown(f"""
    - **리스크 진단:** 대격변기였던 2020년({shock_2020}%)과 2021년({shock_2021}%)에도 지표가 크게 흔들리지 않고 안정적인 기조를 유지했습니다.
    - **재무 제언:** 위기 방어력이 입증된 안전지대입니다. 무리한 확장보다는 장기적인 투자수익률(ROI) 관점으로 안정적인 손익분기점(BEP) 계획을 세우는 것이 적절합니다.
    """)


# =========================================================================
# 7. [위치 이동 및 기능 제한] 10개년 창업 기업 수 추이 차트
# =========================================================================
st.markdown(f"##### 📊 10개년 창업 기업 수 추이 ({selected_minor})")
fig1 = px.line(
    industry_df, x='연도', # 1번 로드 함수에서 '연도'로 통일했으므로 안전하게 '연도' 지정
    y='창업기업수', 
    markers=True, text='창업기업수', 
    template='plotly_white'
)
fig1.update_traces(textposition="top center", line_color="#2b5c8f", line_width=3)

# 마우스 마찰 시 기본 동작을 '드래그 이동(pan)'으로 설정하고 마우스 휠 줌 활성화
fig1.update_layout(
    dragmode='pan',
    xaxis=dict(fixedrange=False),
    yaxis=dict(fixedrange=False)
)

# [핵심] 상단 카메라 캡처 버튼 및 상단 메뉴 툴바 전체를 숨겨서 깔끔하게 마우스 드래그/줌만 남깁니다.
st.plotly_chart(fig1, use_container_width=True, config={
    'displayModeBar': False,  # 툴바 전체 숨김 (캡처 기능 차단)
    'scrollZoom': True        # 마우스 휠 스크롤로 줌인/줌아웃 활성화
})


st.markdown("---")

# 수정된 부분: 닫히지 않았던 맨 마지막 문장을 올바르게 닫아주었습니다.
st.caption("Data Source: 업종별 창업기업수 통계 (2016-2025) | Page 1")
