import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 웹앱 페이지 환경 설정
st.set_page_config(
    page_title="위기 극복 업종 탐색기",
    layout="wide"
)

# 고급스러운 스타일 테마 주입
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    h1 { color: #0f172a !important; font-weight: 800 !important; }
    h3 { color: #334155 !important; font-weight: 600 !important; }
    .guide-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 25px;
        border-left: 5px solid #0f172a;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 로드 및 전처리
@st.cache_data
def load_page_three_data():
    df = pd.read_csv("cleaned_startup_total.csv")
    df['연도'] = df['연도'].astype(int)
    
    # 각 업종별로 2020년 코로나 당시 변동률(Shock)과 10개년 평균 창업수 계산
    metrics = []
    for (major, minor), group in df.groupby(['대분류', '소분류']):
        group = group.sort_values('연도').reset_index(drop=True)
        
        # 2020년 변동률 계산 (2019 -> 2020)
        try:
            val_2019 = group[group['연도'] == 2019]['창업기업수'].values[0]
            val_2020 = group[group['연도'] == 2020]['창업기업수'].values[0]
            shock_2020 = round(((val_2020 - val_2019) / val_2019) * 100, 2)
        except IndexError:
            shock_2020 = 0.0
            
        avg_startups = round(group['창업기업수'].mean(), 1)
        max_startups = group['창업기업수'].max()
        
        metrics.append({
            '대분류': major,
            '세부업종': minor,
            '2020년_코로나_변동률(%)': shock_2020,
            '10개년_평균_창업수(규모)': avg_startups,
            '최대_창업수': max_startups
        })
        
    return pd.DataFrame(metrics), df

summary_df, raw_df = load_page_three_data()

# 3. 페이지 헤더
st.title("🔍 한눈에 보는 산업별 리스크-리턴 지도")
st.subheader("조건별 슬라이더와 다중 선택을 활용해 위기에 강한 업종들을 직접 발굴해보세요.")

# 안내 문구
st.markdown("""
<div class="guide-card">
    <b>💡 데이터 탐험 가이드:</b><br>
    오른쪽 사이드바에서 <b>코로나 변동률 슬라이더</b>를 조절하면 위기 속에서도 살아남거나 성장한 업종들만 스크리닝(필터링)할 수 있습니다.
    경영학에서는 이를 '포트폴리오 분석'이라고 부르며, 어떤 산업이 위험 대비 보상이 좋은지 분석할 때 사용합니다.
</div>
""", unsafe_allow_html=True)

# =========================================================================
# 4. 다양한 인터랙티브 컨트롤러 구성 (사이드바 활용)
# =========================================================================
st.sidebar.header("🎛️ 업종 필터링 조건 설정")

# 컨트롤러 1: 다중 선택 (Multiselect)
all_majors = summary_df['대분류'].unique()
selected_majors = st.sidebar.multiselect(
    "🎯 분석할 대분류 선택 (중복 가능)", 
    options=all_majors, 
    default=['제조업', '서비스업'] # 기본값 설정
)

# 컨트롤러 2: 슬라이더 (Slider) - 코로나 변동률 기준
min_shock = float(summary_df['2020년_코로나_변동률(%)'].min())
max_shock = float(summary_df['2020년_코로나_변동률(%)'].max())

selected_shock_range = st.sidebar.slider(
    "📊 2020년 코로나 변동률(%) 범위",
    min_value=min_shock,
    max_value=max_shock,
    value=(min_shock, max_shock) # 기본값은 전체 범위
)

# 데이터 필터링 적용
filtered_summary = summary_df[
    (summary_df['대분류'].isin(selected_majors)) &
    (summary_df['2020년_코로나_변동률(%)'] >= selected_shock_range[0]) &
    (summary_df['2020년_코로나_변동률(%)'] <= selected_shock_range[1])
]

# =========================================================================
# 5. 메인 시각화 1: 산점도 (Scatter Plot)
# =========================================================================
st.markdown("### 📍 산업별 위험(Risk) vs 규모(Size) 매트릭스")
st.caption("X축은 코로나 때 버틴 힘(오른쪽일수록 강함), Y축은 평균 창업 규모(위쪽일수록 대형 산업)를 뜻합니다. 점의 크기는 역대 최대 창업수입니다.")

if not filtered_summary.empty:
    fig_scatter = px.scatter(
        filtered_summary,
        x='2020년_코로나_변동률(%)',
        y='10개년_평균_창업수(규모)',
        color='대분류',
        size='최대_창업수',
        hover_name='세부업종',
        text='세부업종',
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.add_vline(x=0.0, line_dash="dash", line_color="red") # 0% 기준선
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning("조건에 맞는 업종이 없습니다. 사이드바의 필터 범위를 넓혀보세요!")

st.markdown("---")

# =========================================================================
# 6. 메인 시각화 2: 영역 차트 (Area Chart)로 보는 누적 트렌드
# =========================================================================
st.markdown("### 📈 필터링된 업종들의 10개년 창업 수 누적 변화 추이")
st.caption("위에서 필터링된 세부 업종들이 시간의 흐름에 따라 전체 창업 생태계에서 차지하는 면적(비중)을 시각적으로 관찰합니다.")

# 원본 시계열 데이터에서 필터링된 소분류만 추출
filtered_minors = filtered_summary['세부업종'].unique()
filtered_raw = raw_df[raw_df['소분류'].isin(filtered_minors)].copy()
filtered_raw = filtered_raw.sort_values(['소분류', '연도'])

if not filtered_raw.empty:
    fig_area = px.area(
        filtered_raw,
        x='연도',
        y='창업기업수',
        color='소분류',
        template='plotly_white',
        line_group='소분류'
    )
    st.plotly_chart(fig_area, use_container_width=True)
else:
    st.info("상단 산점도에 표시된 업종이 없으면 누적 영역 차트도 나타나지 않습니다.")

st.markdown("---")
st.caption("Data Source: 업종별 창업기업수 통계 (2016-2025) | Page 3 (인터랙티브 포트폴리오 스크리닝)")
