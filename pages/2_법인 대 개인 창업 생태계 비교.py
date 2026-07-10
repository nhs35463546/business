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
# 9. [더 쉽게 수정됨] 중학생도 이해하는 법인 vs 개인 창업 성적표
# =========================================================================
st.markdown(f"### 📝 **{selected_minor}** 업종의 법인 vs 개인 성적표")

# 법인이 더 잘 버텼을 때 (격차가 0보다 클 때)
if defense_gap > 0:
    st.success("🛡️ 실험 결과: '법인'이라는 형태가 위기를 막아주는 든든한 방패가 되었습니다!")
    st.markdown(f"""
    <div class="compare-card">
        <p style="color:#334155; line-height:1.8; font-size:16px;">
            2020년 코로나19로 경제가 어려웠을 때, <b>법인 창업({corp_shock_2020}%)</b>이 <b>개인 창업({priv_shock_2020}%)</b>보다 
            <b>{defense_gap}%p만큼 충격을 덜 받거나 더 잘 버텨냈습니다.</b> 왜 이런 차이가 났을까요?
        </p>
        <div class="insight-box">
            <h4 style="margin-top:0; color:#0f172a;">💡 중학생 눈높이 경영학 교실</h4>
            <ul style="color:#475569; margin-top:5px; padding-left:20px; line-height:1.7;">
                <li><b>1. 내 전 재산을 지켜주는 안전장치 (유한책임):</b> 법인으로 회사를 차리면, 회사가 망해도 내가 처음에 내기로 한 돈만 잃고 끝납니다. 반면 개인 창업은 회사가 빚을 지면 사장님이 자기 집과 전 재산을 털어서라도 다 갚아야 합니다. 경제가 무서울 때 사람들이 법인을 더 안심하고 선택한 이유입니다.</li>
                <li><b>2. 친구들에게 돈을 모으는 능력 (자본 조달):</b> 법인은 "우리 회사 주식을 살래?"라며 여러 사람이나 기관에서 돈을 모으기가 쉽고, 정부 지원금도 더 많이 받습니다. 이렇게 모아둔 '비상금'이 많다 보니 위기가 와도 쉽게 쓰러지지 않고 창업을 시작할 수 있었습니다.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 개인이 더 잘 버텼을 때 (격차가 0보다 작거나 같을 때)
else:
    st.warning("⚠️ 역발상 결과: 위기 속에서 오히려 '개인 창업'의 빠른 기동성이 빛났습니다!")
    st.markdown(f"""
    <div class="compare-card">
        <p style="color:#334155; line-height:1.8; font-size:16px;">
            예상과 달리, 2020년 위기 속에서 <b>개인 창업({priv_shock_2020}%)</b>이 <b>법인 창업({corp_shock_2020}%)</b>보다 
            <b>{abs(defense_gap)}%p만큼 더 잘 버텼습니다.</b> 개인 창업만의 특별한 생존 비결은 무엇이었을까요?
        </p>
        <div class="insight-box">
            <h4 style="margin-top:0; color:#0f172a;">💡 중학생 눈높이 경영학 교실</h4>
            <ul style="color:#475569; margin-top:5px; padding-left:20px; line-height:1.7;">
                <li><b>1. 1인용 자전거처럼 빠른 방향 전환 (기동성):</b> 법인은 큰 배와 같아서 방향을 바꾸려면 회의도 많이 해야 하고 절차가 복잡합니다. 반면 개인 창업은 사장님 혼자 "오늘부터 비대면 배달 위주로 바꾸자!"라고 빠르게 결정하고 움직일 수 있습니다. 변화에 더 빨리 적응한 것입니다.</li>
                <li><b>2. 어쩔 수 없이 시작한 생계형 창업:</b> 코로나19로 일자리가 줄어들자, 많은 사람들이 먹고살기 위해 소자본으로 작은 가게나 온라인 쇼핑몰을 직접 차려야만 했습니다. 이 때문에 일시적으로 개인 창업 숫자가 많이 늘어난 현상일 수 있습니다.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Data Source: 업종별 창업기업수 통계 (2016-2025) | Page 2 )
