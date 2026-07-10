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
        padding: 25px;
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
st.subheader("회사의 형태(유한책임 제도 및 자본 조달력)에 따른 경제 위기 방어력 분석")
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
st.markdown(f"##### 📊 2020년 코로나19 팬데믹 당시 **[{selected_minor}]** 업종의 형태별 창업 변동률")
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.metric(label="법인 창업 변동률", value=f"{corp_shock_2020}%", delta="법인사업자")
with kpi_col2:
    st.metric(label="개인 창업 변동률", value=f"{priv_shock_2020}%", delta="개인사업자", delta_color="inverse")
with kpi_col3:
    # 구조적 방어력 격차 산출 (법인이 개인보다 얼마나 덜 감소했는지 혹은 더 성장했는지)
    defense_gap = round(corp_shock_2020 - priv_shock_2020, 2)
    st.metric(label="법인의 경제위기 방어 격차(Gap)", value=f"{defense_gap}%p", 
              delta="플러스일수록 법인이 위기에 강함", delta_color="off")

st.markdown("---")

# =========================================================================
# 8. 시각화 섹션 (증감률 차트를 없애고 연도별 창업수 비교 차트만 깔끔하게 배치)
# =========================================================================
st.markdown(f"##### 📊 **[{selected_minor}]** 법인 vs 개인 연도별 창업 기업 수 비교")
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

st.markdown("---")

# =========================================================================
# 9. 다듬어진 경영학적 리스크 리포트 (고등학생 수준에 맞춰 쉽고 명확하게 수정)
# =========================================================================
st.markdown(f"### 📝 **{selected_minor}** 업종의 형태별 경영 리스크 진단 결과")

# 격차가 0보다 클 때 (법인이 더 잘 버텼을 때)
if defense_gap > 0:
    st.success("🛡️ 경영학적 발견: 법인 구조가 가진 '위기 방어 완충 효과'를 확인했습니다.")
    st.markdown(f"""
    <div class="compare-card">
        <p style="color:#334155; line-height:1.8; font-size:16px;">
            2020년 코로나19 경제 충격 당시, <b>법인 창업 변동률({corp_shock_2020}%)</b>이 <b>개인 창업 변동률({priv_shock_2020}%)</b>보다 
            <b>{defense_gap}%p만큼 충격을 덜 받았거나 더 빠르게 회복</b>했습니다. 이는 회사의 경영 구조가 위기를 막아주는 방패 역할을 했음을 보여줍니다.
        </p>
        <div class="insight-box">
            <h4 style="margin-top:0; color:#0f172a;">💡 세부 경영학 분석 및 생기부 탐구 가이드</h4>
            <ul style="color:#475569; margin-top:5px; padding-left:20px; line-height:1.7;">
                <li><b>1. 유한책임(Limited Liability) 제도의 효과:</b> 법인은 개인이 낸 자본금 안에서만 책임을 지면 됩니다. 반면 개인 창업자는 위기가 오면 자신의 전 재산을 잃을 위험이 있습니다. 따라서 경제가 불안할 때 법인 형태가 창업자들에게 두려움을 낮춰주는 안전장치가 됩니다.</li>
                <li><b>2. 다양한 자본 조달(Capital Sourcing) 능력:</b> 법인은 주식을 발행하거나 투자를 유치하고, 정부의 법인 대상 지원금을 받기가 개인 사업자보다 훨씬 유리합니다. 이렇게 모아둔 돈이 위기 상황에서 버틸 수 있는 <b>비상 운전자본(Cash Buffer)</b> 역할을 하여 창업을 무사히 시작할 수 있도록 도왔습니다.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 격차가 0보다 작을 때 (개인이 더 잘 버텼을 때)
else:
    st.warning("⚠️ 역발상 현상: 위기 속에서 오히려 '개인 창업의 신속함과 생계형 창업'이 돋보였습니다.")
    st.markdown(f"""
    <div class="compare-card">
        <p style="color:#334155; line-height:1.8; font-size:16px;">
            예상과 달리, 2020년 위기 속에서 <b>개인 창업 변동률({priv_shock_2020}%)</b>이 <b>법인 창업 변동률({corp_shock_2020}%)</b>보다 
            <b>{abs(defense_gap)}%p만큼 더 잘 버텼습니다.</b> 이는 업종 특성에 따라 개인 창업만의 독특한 생존 방식이 작용했음을 뜻합니다.
        </p>
        <div class="insight-box">
            <h4 style="margin-top:0; color:#0f172a;">💡 세부 경영학 분석 및 생기부 탐구 가이드</h4>
            <ul style="color:#475569; margin-top:5px; padding-left:20px; line-height:1.7;">
                <li><b>1. 빠른 의사결정과 기동성(Agility):</b> 법인은 이사회나 주주총회처럼 복잡한 절차가 필요하지만, 개인 창업은 사장님의 결단으로 시장 진입과 정리가 매우 빠릅니다. 비대면 트렌드 등 변화하는 시장에 신속하게 적응한 결과일 수 있습니다.</li>
                <li><b>2. 구조조정으로 인한 생계형 창업:</b> 코로나19로 고용 시장이 얼어붙으면서, 생계를 위해 어쩔 수 없이 소자본으로 시작하는 '생계형 개인 창업'이 일시적으로 늘어나 지표가 방어된 현상일 수 있습니다.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Data Source: 법인/개인별 창업기업수 통계 (2016-2025) | Page 2 (경영 구조적 리스크 분석)")
