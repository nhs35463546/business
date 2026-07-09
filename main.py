import streamlit as st

# 1. 웹앱 전체 환경 설정 (최상단 필수)
st.set_page_config(
    page_title="Shock & Resilience 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 고급스러운 금융/경영 대시보드 테마 및 원형(Circle) 디자인 CSS 주입
st.markdown("""
    <style>
    /* 메인 화면 전체 배경을 금융 분석 플랫폼 느낌의 연한 블루그레이 톤으로 변경 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* [색상 수정] 타이틀 폰트 색상을 블랙에 가까운 묵직한 다크 네이비로 변경 */
    h1 {
        color: #000033 !important;
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
        margin-bottom: 35px;
        border-left: 5px solid #1e3a8a; /* 테두리도 묵직한 네이비로 매칭 */
    }
    
    /* 가치관 표현을 위한 세련된 원형 컨테이너 스타일 */
    .circle-container {
        display: block;
        margin: 0 auto;
        text-align: center;
    }
    
    .circle-card {
        background: #ffffff;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        display: table-cell;
        vertical-align: middle;
        text-align: center;
        margin: 0 auto;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -2px rgba(15, 23, 42, 0.04);
        border: 4px solid #0f172a; /* 원형 테두리도 바뀐 메인 색상과 통일 */
    }
    
    /* 원형 내 이모지 스타일 */
    .circle-emoji {
        font-size: 40px;
        margin-bottom: 10px;
        display: block;
    }
    
    /* 원형 내 글자 스타일 */
    .circle-text {
        color: #0f172a;
        font-size: 15px;
        font-weight: 700;
        line-height: 1.4;
        padding: 0 15px;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 메인 대문 제목 및 [수정] 이해하기 쉬운 부제목
st.title("📉 Shock & Resilience")
st.subheader("위기에 강한 업종은 어디일까? 10개년 데이터로 보는 경제 충격과 창업 생존 지도")
st.markdown("---")

# 4. 인트로 섹션 (정돈된 프로젝트 기획 배경 카드)
st.markdown("""
<div class="intro-card">
    <h3 style="margin-top:0; color:#1e3a8a;">🎯 프로젝트 기획 배경</h3>
    <p style="color:#475569; line-height:1.7; margin-bottom:10px;">
        경영·회계학적으로 기업의 생존과 성장은 단순히 유행을 따르는 것이 아니라, 
        <b>대외적인 리스크 요인을 얼마나 정밀하게 예측하고 방어하느냐</b>에 따라 결정됩니다.
    </p>
    <p style="color:#475569; line-height:1.7;">
        본 대시보드는 <b>지난 10개년(2016-2025) 중소벤처기업부의 데이터</b>를 기반으로, 우리 경제가 마주했던 대표적인 두 번의 대격변기인 
        <b>2020년 코로나19 팬데믹 쇼크(대면 제한)</b>와 <b>2021년 초저금리 유동성 과열기(자산 시장 급변)</b>를 집중 추적합니다.
    </p>
    <p style="color:#0f172a; font-weight:600; margin-bottom:0; margin-top:15px;">
        💡 왼쪽 사이드바 메뉴의 각 Page로 이동하여 외부 충격에 가장 단단한 '재무적 안전지대'를 직접 탐색해 보세요.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 5. 핵심 학술적 가치 (3구 원형 배지 레이아웃)
st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>🏢 경영·회계학적 리스크 관리 핵심 가치</h3>", unsafe_allow_html=True)

empty_left, kpi_col1, kpi_col2, kpi_col3, empty_right = st.columns([1, 2, 2, 2, 1])

with kpi_col1:
    st.markdown("""
    <div class="circle-container">
        <div class="circle-card">
            <span class="circle-emoji">📊</span>
            <span class="circle-text">1. 기업 가치 및<br>수익성 보호</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown("""
    <div class="circle-container">
        <div class="circle-card">
            <span class="circle-emoji">🛡️</span>
            <span class="circle-text">2. 지속가능성 및<br>회복탄력성 확보</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown("""
    <div class="circle-container">
        <div class="circle-card">
            <span class="circle-emoji">🤝</span>
            <span class="circle-text">3. 신뢰 및<br>평판 자본 축적</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Data Source: 업종별 창업기업수 통계 (2016-2025) | 본 대시보드는 경영·회계 및 데이터 분석 전공 탐구 목적으로 제작되었습니다.")
