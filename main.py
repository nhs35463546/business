import streamlit as st

# 1. 웹앱 전체 환경 설정 (최상단 필수)
st.set_page_config(
    page_title="Shock & Resilience 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 고급스러운 금융/경영 대시보드 테마 CSS 주입 (그라데이션 및 카드 UI)
st.markdown("""
    <style>
    /* 메인 화면 전체 배경을 금융 분석 플랫폼 느낌의 연한 블루그레이 톤으로 변경 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* 타이틀 폰트 및 색상 강조 (딥 네이비) */
    h1 {
        color: #1e3a8a !important;
        font-weight: 800 !important;
    }
    
    /* 부제목 색상 */
    h3 {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    
    /* 프로젝트 기획 배경을 감싸는 입체적인 카드 스타일 */
    .intro-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 25px;
        border-left: 5px solid #2563eb;
    }
    
    /* 하단 3대 핵심 가치관 전용 상단 라인 포인트 카드 스타일 */
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

# 4. 인트로 섹션 (정돈된 프로젝트 기획 배경 카드)
st.markdown("""
<div class="intro-card">
    <h3 style="margin-top:0; color:#2563eb;">🎯 프로젝트 기획 배경</h3>
    <p style="color:#475569; line-height:1.7; margin-bottom:10px;">
        경영·회계학적으로 기업의 생존과 성장은 단순히 유행을 따르는 것이 아니라, 
        <b>대외적인 리스크 요인을 얼마나 정밀하게 예측하고 방어하느냐</b>에 따라 결정됩니다.
    </p>
    <p style="color:#475569; line-height:1.7;">
        본 대시보드는 <b>지난 10개년(2016-2025) 중소벤처기업부의 데이터</b>를 기반으로, 우리 경제가 마주했던 대표적인 두 번의 대격변기인 
        <b>2020년 코로나19 팬데믹 쇼크(대면 제한)</b>와 <b>2021년 초저금리 유동성 과열기(자산 시장 급변)</b>를 집중 추적합니다.
    </p>
    <p style="color:#1e3a8a; font-weight:600; margin-bottom:0; margin-top:15px;">
        💡 왼쪽 사이드바 메뉴의 각 Page로 이동하여 외부 충격에 가장 단단한 '재무적 안전지대'를 직접 탐색해 보세요.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 5. 핵심 학술적 가치 (새로운 3대 핵심 가치 매칭 및 간결화)
st.markdown("### 🏢 경영·회계학적 리스크 관리 핵심 가치")

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown("""
    <div class="value-card">
        <h4 style="color:#1e3a8a; margin-top:0;">📊 1. 기업 가치 및 수익성 보호</h4>
        <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:0;">
            거시경제 충격 시나리오 속에서 업종별 창업 추이를 예측함으로써 비즈니스의 불확실성을 최소화하고, 재무적 손실을 선제적으로 방어하여 기업 가치를 보호합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown("""
    <div class="value-card">
        <h4 style="color:#1e3a8a; margin-top:0;">🛡️ 2. 지속가능성 및 회복탄력성 확보</h4>
        <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:0;">
            경기 하강 국면과 충격 여파 속에서도 산업 생태계가 무너지지 않고 빠르게 연착륙할 수 있도록, 업종별 기초 체력과 지속가능성(Going Concern)을 진단합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown("""
    <div class="value-card">
        <h4 style="color:#1e3a8a; margin-top:0;">🤝 3. 신뢰 및 평판 자본 축적</h4>
        <p style="color:#475569; font-size:14px; line-height:1.6; margin-bottom:0;">
            리스크 변동성에 적합한 자본 구조(개인 vs 법인) 선택 가이드를 제시하여 이해관계자의 신뢰를 구축하고, 위기 대응 역량을 입증함으로써 기업의 평판 자본을 축적합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Data Source: 중소벤처기업부 창업기업동향 통계 (2016-2025) | 본 대시보드는 경영·회계 및 데이터 분석 전공 탐구 목적으로 제작되었습니다.")
