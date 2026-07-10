import streamlit as st

# 1. 웹앱 전체 환경 설정 (최상단 필수)
st.set_page_config(
    page_title="Shock & Resilience 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 고급스러운 금융/경영 대시보드 테마 및 원형(Circle) 디자인 CSS 주입
st.markdown(""
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
        display: table-cell;
        vertical-align: middle;
        text-align: center;
        margin: 0 auto;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -2px rgba(15, 23,
