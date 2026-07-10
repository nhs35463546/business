import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 웹앱 페이지 환경 설정 (멀티페이지의 개별 페이지용 설정)
st.set_page_config(
    page_title="법인 vs 개인 위기 대응력 비교",
    layout="wide"
)

# 2. 첫 페이지와 톤앤매너를 맞추기 위한 고급스러운 CSS 주입
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    h1 {
        color: #0f172a !important;
        font-weight: 800 !important;
    }
    h3 {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    .compare-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border-top: 4px solid #1e3a8a;
    }
    .insight-box {
        background-color: #f8fafc;
        border-left: 5px solid #0f172a;
        padding: 15px;
        border-radius: 4px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수 (법인 및 개인 데이터 동시 캐싱)
@st.cache_data
def load_comparison_data():
    try:
        corp = pd.read_csv("cleaned_startup_corporate.csv")
        priv = pd.read_csv("cleaned_startup_private.csv")
        
        # 연도 컬럼 타입을 문자열로 통일
        corp['연도'] = corp['연도'].astype(str)
        priv['연도'] = priv['연도'].astype(str)
        return corp, priv
    except Exception as e:
        st.error(f"데이터 파일을 불러오는 중 오류가 발생했습니다: {e}")
        st.stop()

df_corp, df_priv = load_comparison_data()

# 4. 페이지 헤더
st.title("⚖️ 법인 vs 개인 창업 구조별 위기 대응력 비교")
st.subheader("경영 구조(유한책임 및 자본 규모)에 따른 거시경제 충격 방어력 분석")
st.markdown("---")

# 5. 분석 대상 업종 선택 (메인 화면 배치)
st.subheader("🔍 분석 대상 업종 선택")
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    major_categories = df_corp['대분류'].unique()
    selected_major = st.selectbox("🎯 산업 대분류 선택", major_categories, key="comp_major")

# 대분류에 따른 소분류 필터링 (법인 데이터 기준)
sub_df_corp = df_corp[df_corp['대분류'] == selected_major]

with filter_col2:
    selected_minor = st.selectbox("🔎 세부 업종 (소분류) 선택", sub_df_corp['소분류'].unique(), key="comp_minor")

# =========================================================================
# 6. 데이터 전처리 및 증감률(변동률) 계산 프로세스
# =========================================================================
def process_industry_data(df, major, minor, label):
    # 필터링 및 복사
    filtered = df[(df['대분류'] == major) & (df['소분류'] == minor)].copy()
    
    # 연도 정렬 보정
    filtered['연도_int'] = filtered['연도'].astype(int)
    filtered = filtered.sort_values(by='연도_int').reset_index(drop=True)
    filtered['연도'] = filtered['연도_int'].astype(str)
    
    # 증감률 계산
    pct_changes = [0.0]
    for i in range(1, len(filtered)):
        prev_val = filtered.loc[i-1, '창업기업수']
        curr_val = filtered.loc[i, '창업기업수']
        if prev_val > 0:
            change = ((curr_val - prev_val) / prev_val) * 100
            pct_changes.append(round(change, 2))
        else:
            pct_changes.append(0.0)
            
    filtered['증감률(%)'] = pct_changes
    filtered['경영형태'] = label
    return filtered

# 법인 및 개인 각각의 시계열 데이터 가공
industry_corp = process_industry_data(df_corp, selected_major, selected_minor, "법인(Corporate)")
industry_priv = process_industry_data(df_priv, selected_major, selected_minor, "개인(Private)")

# 두 데이터를 하나로 병합 (시각화용)
combined_df = pd.concat([industry_corp, industry_priv]).reset_index(drop=True)

# 2020년 코로나 쇼크기 변동률 추출
try:
    corp_shock_2020 = industry_corp[industry_corp['연도'] == '2020']['증감률(%)'].values[0]
    priv_shock_2020 = industry_priv[industry_priv['연도'] == '2020']['증감률(%)'].values[0]
except IndexError:
    corp_shock_2020, priv_shock_2020 = 0.0, 0.0

# =========================================================================
# 7. 핵심 비교 지표 (KPI 스코어보드)
# =========================================================================
st.markdown(f"##### 📊 2020년 코로나19 팬데믹 쇼크 당시 **[{selected_minor}]** 업종의 형태별 변동률")
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.metric(label="법인 창업 변동률", value=f"{corp_shock_2020}%", delta="법인사업자")
with kpi_col2:
    st.metric(label="개인 창업 변동률", value=f"{priv_shock_2020}%", delta="개인사업자", delta_color="inverse")
with kpi_col3:
    # 구조적 방어력 격차 산출 (법인이 개인보다 얼마나 덜 감소했는지 혹은 더 성장했는지)
    defense_gap = round(corp_shock_2020 - priv_shock_2020, 2)
    st.metric(label="법인의 구조적 방어력 격차(Gap)", value=f"{defense_gap}%p", 
              delta="플러스일수록 법인이 위기에 강함", delta_color="off")

st.markdown("---")

# =========================================================================
# 8. 시각화 섹션 (Grouped Bar Chart & Line Chart)
# =========================================================================
chart_tab1, chart_tab2 = st.tabs(["📊 연도별 창업수 비교 (규모)", "📈 연도별 증감률 추이 (속도)"])

with chart_tab1:
    st.markdown(f"##### **[{selected_minor}]** 법인 vs 개인 연도별 창업 기업 수 비교")
    fig_bar = px.bar(
        combined_df,
        x='연도',
        y='창업기업수',
        color='경영형태',
        barmode='group',
        template='plotly_white',
        color_discrete_sequence=['#1e3a8a', '#94a3b8'] # 다크네이비와 실버그레이 매칭
    )
    fig_bar.update_layout(dragmode='pan')
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': True})

with chart_tab2:
    st.markdown(f"##### **[{selected_minor}]** 외부 충격에 따른 전년 대비 증감률(%) 추이 비교")
    fig_line = px.line(
        combined_df,
        x='연도',
        y='증감률(%)',
        color='경영형태',
        markers=True,
        template='plotly_white',
        color_discrete_sequence=['#1e3a8a', '#e11d48'] # 법인은 네이비, 개인은 경고의 의미로 레드 계열 매칭
    )
    # 0% 기준선 추가하여 가독성 증대
    fig_line.add_hline(y=0.0, line_dash="dash", line_color="gray")
    fig_line.update_layout(dragmode='pan')
    st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': True})

st.markdown("---")

# =========================================================================
# 9. 알고리즘 기반 경영학적 리스크 리포트 (학생 탐구 핵심 섹션)
# =========================================================================
st.markdown(f"### 📝 **{selected_minor}** 업종의 경영 구조적 리스크 관리 진단서")

# 경영학적 해석 자동화 분기문
if corp_shock_2020 > priv_shock_2020:
    st.success("🛡️ 경영학적 실증: 법인 구조의 '위기 완충(Buffer) 효과' 확인")
    st.markdown(f"""
    <div class="compare-card">
        <p style="color:#334155; line-height:1.7;">
            2020년 팬데믹 쇼크 당시, <b>법인 창업({corp_shock_2020}%)</b>이 <b>개인 창업({priv_shock_2020}%)</b>에 비해 
            <b>{defense_gap}%p만큼 충격을 덜 받았거나 더 빠르게 방어</b>해 냈습니다. 이는 경영학 및 회계학적으로 매우 의미 있는 구조적 차이를 증명합니다.
        </p>
        <div class="insight-box">
            <b>💡 세부 경영학적 분석 및 학종 탐구 가이드:</b>
            <ul style="color:#475569; margin-top:5px; padding-left:20px; line-height:1.6;">
                <li><b>유한책임(Limited Liability)의 장벽 완화:</b> 법인 창업자는 출자 자본 한도 내에서만 책임을 지므로, 거시경제적 불확실성이 극대화된 시기에도 개인 자산 전체를 담보로 잡아야 하는 개인 창업자에 비해 리스크 테이킹(Risk-taking) 장벽이 낮습니다.</li>
                <li><b>자본 조달(Capital Sourcing)의 다양성:</b> 법인은 주식 발행, 회사채, 기관 투자 유치 및 정부의 중소기업 정책자금(융자) 지원을 받기가 개인 사업자보다 훨씬 유리합니다. 대격변기에 확보된 이러한 자금력이 비상 운전자본(Cash Buffer) 역할을 하여 창업 진입 유인을 유지시켰을 가능성이 높습니다.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif corp_shock_2020 < priv_shock_2020:
    st.warning("⚠️ 역발상 현상: 위기 상황 속 '개인 창업의 기동성 및 생계형 창업' 집중")
    st.markdown(f"""
    <div class="compare-card">
        <p style="color:#334155; line-height:1.7;">
            일반적인 예상과 달리 2020년 쇼크기에 <b>개인 창업의 방어력({priv_shock_2020}%)</b>이 <b>법인 창업({corp_shock_2020}%)</b>보다 우세했습니다. 
            이는 해당 업종의 특성과 거시경제 충격이 맞물려 나타난 독특한 경영학적 현상입니다.
        </p>
        <div class="insight-box">
            <b>💡 세부 경영학적 분석 및 학종 탐구 가이드:</b>
            <ul style="color:#475569; margin-top:5px; padding-left:20px; line-height:1.6;">
                <li><b>생계형 창업 및 의사결정의 신속성:</b> 고용 시장이 위축되면서 대안으로 선택하는 '생계형 개인 창업'이 급증했을 수 있습니다. 또한, 법인은 이사회 및 주주총회 등 복잡한 설립 프로세스가 필요한 반면, 개인은 경영자의 단독 결단으로 시장 진입과 철수가 매우 신속(Agility)하기 때문에 나타난 결과일 수 있습니다.</li>
                <li><b>소규모 자본의 기회 포착:</b> 대규모 고정비(임차료, 대규모 인건비)가 들어가는 법인 모델과 달리, 최소 자본과 비대면 플랫폼을 활용한 소규모 개인 창업이 위기 속 틈새시장을 더 빠르게 공략했을 가능성이 있습니다.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("📊 균형 현상: 경영 구조와 무관한 산업 전반의 시스템적 리스크(Systemic Risk)")
    st.markdown(f"""
    <div class="compare-card">
        <p style="color:#334155; line-height:1.7;">
            법인과 개인 창업 모두 동일한 수준의 충격을 받았습니다. 이는 경영 형태나 지배구조의 차이로 극복할 수 없는 
            <b>산업 전체의 강력한 시스템적 리스크(Systemic Risk)</b>가 작용했음을 시사합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Data Source: 법인/개인별 창업기업수 통계 (2016-2025) | Page 2 (경영 구조적 리스크 분석)")
