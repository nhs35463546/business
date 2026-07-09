import streamlit as st

# 1. 브라우저 탭에 표시될 메인 설정 (가장 위에 배치해야 합니다)
st.set_page_config(
    page_title="Shock & Resilience 대시보드",
    layout="wide", # 화면을 넓게 사용
    initial_sidebar_state="expanded"
)

# 2. 메인 화면 제목 (Title)
st.title("📉 Shock & Resilience")

# 3. 메인 화면 부제목 (Subheader)
st.subheader("10개년 데이터로 보는 거시경제 충격과 업종별 창업 저항력 지도")

# 4. 프로젝트 설명 (Markdown - 가독성을 높여줍니다)
st.markdown("""
본 대시보드는 **2020년 코로나19 팬데믹(대면 제한)** 및 **2021년 초저금리 유동성 과열** 등 
대외적 거시경제 충격이 국내 창업 생태계에 미친 영향을 분석합니다. 

경영·회계적 리스크 관리 관점에서 업종별 저항력을 확인하고 안전한 창업 타이밍을 탐색해 보세요.👋
""")

# 구분을 위한 깔끔한 가로선
st.markdown("---")

# 이 아래에 사이드바 및 그래프 출력 코드가 이어집니다.
st.write("⬅️ 왼쪽 사이드바에서 업종을 선택하시면 분석 리포트가 시작됩니다.")
