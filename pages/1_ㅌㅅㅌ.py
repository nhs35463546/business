import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 캐시 로드 함수
@st.cache_data
def load_page_one_data():
    # 코랩에서 정제한 '전체' 데이터셋을 불러옵니다.
    df = pd.read_csv("cleaned_startup_total.csv")
    df['연도'] = df['연度'].astype(str) if '연度' in df.columns else df['연도'].astype(str)
    return df

try:
    df = load_page_one_data()
except Exception as e:
    st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.info("루트 폴더에 'cleaned_startup_total.csv' 파일이 업로드되어 있는지 확인해주세요.")
    st.stop()

# 2. [수정] 페이지 상단 제목 및 레이아웃
st.title("📈 업종별 창업 기업 수 추이 및 외부 충격 영향 진단")
st.caption("Page 1: Shock & Resilience 리스크 진단 화면")
st.markdown("""
특정 업종을 선택하여 지난 10개년간의 창업 기업 수 변화 추이를 관찰하고, 
대외적 거시경제 충격(2020년 코로나 팬데낵, 2021년 자산 과열기)이 발생했을 때 해당 산업이 받은 영향을 진단합니다.
""")
st.markdown("---")

# 3. 사이드바 - 업종 필터 기능 구현
st.sidebar.title("🔍 업종 선택")
major_categories = df['대분류'].unique()
selected_major = st.sidebar.selectbox("🎯 산업 대분류", major_categories)

# 선택한 대분류 내의 소분류 필터링
sub_df = df[df['대분류'] == selected_major]
selected_minor = st.sidebar.selectbox("🔎 세부 업종 (소분류)", sub_df['소분류'].unique())

# 4. 전년 대비 증감률(%) 연산 프로세스 (내부 리포트 진단용 로직 유지)
industry_df = sub_df[sub_df['소분류'] == selected_minor].sort_values(by='연도').reset_index(drop=True)

pct_changes = [0.0]  # 2016년은 기준점이 없으므로 0% 세팅
for i in range(1, len(industry_df)):
    prev_val = industry_df.loc[i-1, '창업기업수']
    curr_val = industry_df.loc[i, '창업기업수']
    if prev_val > 0:
        change = ((curr_val - prev_val) / prev_val) * 100
        pct_changes.append(round(change, 2))
    else:
        pct_changes.append(0.0)

industry_df['증감률(%)'] = pct_changes

# 5. [수정] 핵심 재무 지표 (KPI) 스코어보드 - 2025년 지표 카드 삭제
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

# 6. [수정] 10개년 창업 기업 수 추이 차트 (화면 전체 너비 활용)
st.markdown(f"##### 📊 10개년 창업 기업 수 추이 ({selected_minor})")
fig1 = px.line(
    industry_df, x='연도', y='창업기업수', 
    markers=True, text='창업기업수', 
    template='plotly_white'
)
fig1.update_traces(textposition="top center", line_color="#2b5c8f", line_width=3)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# 7. 알고리즘 기반 경영·회계적 리스크 분석 보고서 자동 출력
st.subheader("💡 경영 리스크 관리 가이드 보고서")
st.markdown(f"### 🔍 **{selected_minor}** 업종의 거시경제 스트레스 테스트 결과")

# 위기 시 변동폭 절대값이 15%를 넘어가면 고위험 경기민감형으로 판명
if abs(shock_2020) >= 15 or abs(shock_2021) >= 15:
    st.error("🚨 본 업종은 외부 충격에 취약한 [고변동성 / 경기 민감 업종] 성향을 나타냅니다.")
    st.markdown(f"""
    - **리스크 진단:** 2020년 팬데믹 당시 **{shock_2020}%**, 2021년 과열기 당시 **{shock_2021}%**의 급격한 창업 수 변동을 기록했습니다. 외부 환경 조건에 수요와 공급이 매우 민감하게 반응하는 산업 구조입니다.
    - **재무적 제언:** 경기 하강 국면에서 변동성이 극되화되어 초기 투자금 회수 리스크가 커질 위험이 높습니다. 고정비(임대료, 고정 인건비) 비율을 최소화하고, 경영난에 대비해 최소 3~6개월을 버틸 수 있는 **비상 운전자본(Cash Buffer)**을 일반 업종보다 두텁게 확보해야 지속가능성(Going Concern)을 유지할 수 있습니다.
    """)
else:
    st.success("🛡️ 본 업종은 대외 위기에도 견고한 [저변동성 / 불황 저항형 업종] 성향을 나타냅니다.")
    st.markdown(f"""
    - **리스크 진단:** 대격변기였던 2020년({shock_2020}%)과 2021년({shock_2021}%)에도 창업 지표가 크게 동요하지 않고 안정적인 기조를 유지했습니다. 경기 흐름과 무관하게 사회적으로 상시 요구되는 필수재 혹은 인프라 성격의 비즈니스 모델입니다.
    - **재무적 제언:** 위기 상황에서의 리스크 방어력이 입증된 안전지대입니다. 다만, 자산 호황기에도 폭발적인 성장을 기대하기는 어려울 수 있으므로, 단기 대박을 노리기보다는 장기적이고 점진적인 투자수익률(ROI) 관점으로 안정적인 손익분기점(BEP) 계획을 세우는 것이 적절합니다.
    """)

st.markdown("---")
st.caption("Data Source: 중소벤처기업부 창업기업동향 통계 | 본 화면은 다중 페이지 시스템 중 Page 1에 해당합니다.")
