import streamlit as st

# 1. 웹앱 전체 환경 설정 (최상단 필수)
st.set_page_config(
    page_title="Shock & Resilience 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 분위기에 맞는 고급스러운 금융/경영 대시보드 테마 CSS 주입
# 배경에 미세한 그라데이션을 넣고 카드 레이아웃의 가독성을 높입니다.
st.markdown("""
    <style>
    /* 메인 화면 전체 배경을 연한 차콜/그레이 톤으로 세련되게 변경 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* 타이틀 폰트 및 색상 강조 (네이비 컬러) */
    h1 {
        color: #1e3a8a !important;
        font-weight: 800 !important;
    }
    
    /* 부제목 색상 (차분한 블루 그레이) */
    h3 {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    
    /* 카드 형태의 텍스트 상자 스타일 정의 */
    .intro-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 25px;
        border-left: 5px solid #2563eb;
    }
    
    /* 가치관 요약 카드 스타일 정의 */
    .value-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-top: 4px solid #1e3a8a;
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 메인 대문 제목 및 부제목
st.title("📉 Shock & Resilience")
st.subheader("거시경제 충격에 따른 산업별 창업 저항력 및 자본 구조 분석 대시보드")
st.markdown("---")

# 4. 인트로 섹션 (커스텀 CSS 카드 적용)
st.markdown("""
<div class="intro-card">
    <h3 style="margin-top:0; color:#2563eb;">🎯 프로젝트 기획 배경</h3>
    <p style="color:#475569; line-height:1.7;">
        대부분의 예비 창업자들은 단순히 당시의 유행이나 진입 장벽만을 고려하여 창업 형태(개인 vs 법인)와 업종을 선택합니다. 
        그러나 경영·회계학적으로 기업의 생존은 <b>외부 리스크에 대한 방어력(Resilience)</b>과 <b>지속가능성(Going Concern)</b>에 의해 결정됩니다.
    </p>
    <p style="color:#475569; line-height:1.7;">
        본 대시보드는 <b>지난 10개년(2016-2025) 중소벤처기업부의 창업기업동향 데이터</b>를 기반으로 설계되었습니다. 
        특히 우리 경제가 마주했던 두 번의 대격변기를 집중 조명하여 분석합니다:<br>
        1. <b>2020년 코로나19 팬데믹 쇼크 (대면 제한 리스크)</b><br>
        2. <b>2021년 초저금리 유동성 과열기 (자산 시장 변동 리스크)</b>
    </p>
    <p style="color:#1e3a8a; font-weight:600; margin-bottom:0;">
        💡 데이터가 증명하는 시장의 흔적을 통해, 외부 충격에 가장 튼튼한 '재무적 안전지대'가 어디인지 왼쪽 사이드바 메뉴를 통해 직접 탐색해 보세요.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 5. 핵심 학술적 가치 (3열 카드 디자인 적용)
st.markdown("### 🏢 경영·회계학적 리스크 관리 핵심 가치")

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown("""
    <div class="value-card">
        <h4 style="color:#1e3a8a; margin-top:0;">🛡️ 운전자본의 중요성 (Cash Buffer)</h4>
        <p style="color:#64748b; font-size:14px; line-height:1.6;">
            변동성이 극심한 경기 민감 업종일수록, 예기치 못한 쇼크 상황에서 3~6개월간 고정비(임대료, 인건비)를 버텨낼 수 있는 충분한 현금성 완충 자산이 필수적임을 데이터로 입증합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown("""
    <div class="value-card">
        <h4 style="color:#1e3a8a; margin-top:0;">⚙️ 자본 구조와 위험 분산</h4>
        <p style="color:#64748b; font-size:14px; line-height:1.6;">
            개인사업자와 법인사업자의 재무적 성향 차이를 분석합니다. 외부 투자 유치 및 리스크 분산에 유리한 법인 구조가 대외 경제 충격 속에서 어떤 생존력 차이를 만들어내는지 확인합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown("""
    <div class="value-card">
        <h4 style="color:#1e3a8a; margin-top:0;">📈 지속가능성 (Going Concern)</h4>
        <p style="color:#64748b; font-size:14px; line-height:1.6;">
            단기적인 유행성 창업을 넘어, 경기 하강 국면에서도 꺾이지 않고 상시적인 수요를 창출해 내는 '불황 저항형' 산업군의 특징과 손익분기점(BEP) 관리 전략을 제언합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Data Source: 중소벤처기업부 창업기업동향 통계 (2016-2025) | 본 대시보드는 경영·회계 및 데이터 분석 전공 탐구 목적으로 제작되었습니다.")
