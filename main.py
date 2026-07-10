import streamlit as st

# 1. 웹앱 전체 환경 설정 (최상단 필수)
st.set_page_config(
    page_title="Shock & Resilience 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 고급스러운 금융/경영 대시보드 테마 및 원형(Circle) 디자인 CSS 주입
# 수정된 부분: ""를 """로 변경하고 unsafe_allow_html=True를 추가했습니다.
st.markdown("""
    <style>
    /* 메인 화면 전체 배경을 금융 분석 플랫폼 느낌의 연한 블루그레이 톤으로 변경 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* 타이틀 폰트 색상을 블랙에 가까운 묵직한 다크 네이비로 변경 */
    h1 {
        color: #0f172a !important;
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
        border-left: 5px solid #1e3a8a;
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
        display: inline-block; /* table-cell 대신 레이아웃 잡기 편한 inline-block으로 수정 */
        vertical-align: middle;
        text-align: center;
        margin: 10px;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -2px rgba(15, 23, 42, 0.05);
        padding-top: 70px; /* 원 안의 글자 중앙 정렬용 여백 추가 */
        box-sizing: border-box;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 3. 메인 화면 콘텐츠 예시 (코드가 잘 작동하는지 확인용)
st.title("Shock & Resilience 대시보드")
st.subheader("금융 및 경영 리스크 분석 플랫폼")

st.markdown("""
<div class="intro-card">
    <h4>프로젝트 기획 배경</h4>
    <p>본 대시보드는 외부 충격(Shock)에 대한 기업 및 시장의 회복탄력성(Resilience)을 측정하고 시각화합니다.</p>
</div>
""", unsafe_allow_html=True)

# 원형 카드 배치 예시
st.write("### 핵심 가치관")
st.markdown("""
<div class="circle-container">
    <div class="circle-card">
        <strong>Stability</strong><br>안정성
    </div>
    <div class="circle-card">
        <strong>Flexibility</strong><br>유연성
    </div>
    <div class="circle-card">
        <strong>Growth</strong><br>성장성
    </div>
</div>
""", unsafe_allow_html=True)
