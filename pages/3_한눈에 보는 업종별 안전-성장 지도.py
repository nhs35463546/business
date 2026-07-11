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
    try:
        df = pd.read_csv("cleaned_startup_total.csv")
        df['연도'] = df['연度'].astype(int) if '연度' in df.columns else df['연도'].astype(int)
        
        metrics = []
        for (major, minor), group in df.groupby(['대분류', '소분류']):
            group = group.sort_values('연도').reset_index(drop=True)
            
            try:
                val_2019 = group[group['연도'] == 2019]['창업기업수'].values[0]
                val_2020 = group[group['연도'] == 2020]['창업기업수'].values[0]
                shock_2020 = round(((val_2020 - val_2019) / val_2019) * 100, 2)
            except IndexError:
                shock_2020 = 0.0
                
            avg_startups = round(group['창업기업수'].mean(), 1)
            max_startups = group['창업기업su'] if '창업기업su' in group.columns else group['창업기업수'].max()
            if not isinstance(max_startups, (int, float)):
                max_startups = group['창업기업수'].max()
            
            metrics.append({
                '대분류': major,
                '세부업종': minor,
                '2020년_코로나_변동률(%)': shock_2020,
                '10개년_평균_창업수(규모)': avg_startups,
                '최대_창업수': max_startups
            })
            
        return pd.DataFrame(metrics), df
    except Exception as e:
        st.error(f"데이터를 로드하는 중 에러가 발생했습니다: {e}")
        st.stop()

summary_df, raw_df = load_page_three_data()

# 3. 페이지 헤더
st.title("📍 한눈에 보는 업종별 안전-성장 지도")
st.subheader("위기 속에서도 안전하게 잘 성장한 업종들을 직접 찾아보세요.")

# 안내 문구
st.markdown("""
<div class="guide-card">
    <b>💡 데이터 탐험 가이드:</b><br>
    1. 바로 아래 <b>'🎯 분석할 대분류 선택'</b>에서 보고 싶은 산업군을 먼저 골라보세요.<br>
    2. <b>'코로나 전과 후 창업 변화율'</b> 슬라이더를 조절하면 위기 속에서도 살아남은 업종들이 실시간으로 정렬됩니다!
</div>
""", unsafe_allow_html=True)

# 4. 필터 통합 섹션
filter_col1, filter_col2 = st.columns([1, 1])

with filter_col1:
    st.markdown("##### 🎯 분석할 대분류 선택")
    all_majors = summary_df['대분류'].unique() if not summary_df.empty else []
    selected_majors = st.multiselect(
        "원하는 산업 대분류를 선택하세요 (중복 가능)", 
        options=all_majors, 
        default=['제조업', '서비스업'] if '제조업' in all_majors else all_majors[:2]
    )

with filter_col2:
    st.markdown("##### 📊 코로나 전과 후 창업 변화율(%) 범위 설정")
    
    min_shock = -100.0
    max_shock = 100.0
    
    if '2020년_코로나_변동률(%)' in summary_df.columns:
        valid_shocks = summary_df['2020년_코로나_변동률(%)'].dropna()
        if not valid_shocks.empty:
            try:
                min_shock = float(valid_shocks.min())
                max_shock = float(valid_shocks.max())
                if min_shock == max_shock:
                    min_shock -= 10.0
                    max_shock += 10.0
            except Exception:
                pass

    selected_shock_range = st.slider(
        "오른쪽으로 갈수록 코로나 이후 창업이 더 많이 늘어난 업종입니다",
        min_value=min_shock,
        max_value=max_shock,
        value=(min_shock, max_shock)
    )

# 데이터 필터링 적용
filtered_summary = summary_df[
    (summary_df['대분류'].isin(selected_majors)) &
    (summary_df['2020년_코로나_변동률(%)'] >= selected_shock_range[0]) &
    (summary_df['2020년_코로나_변동률(%)'] <= selected_shock_range[1])
]

st.markdown("---")

# 5. 메인 시각화 1: 산점도 사분면 차트
st.markdown("### 📍 업종별 위험(Risk) vs 규모(Size) 사분면 차트")
st.caption("빨간 점선 우측에 있을수록 코로나 위기를 잘 버틴 안전한 업종입니다. (마우스 스크롤로 확대/축소 가능)")

st.markdown("""
> ➡️ **오른쪽(X축)으로 갈수록:** 위기 저항력(안전성)이 높음  
> ⬆️ **위쪽(Y축)으로 갈수록:** 시장 규모가 큼
""")

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
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig_scatter.update_traces(
        textposition='top center',
        marker=dict(line=dict(width=1, color='DarkSlateGrey'))
    )
    
    fig_scatter.add_hline(y=0, line_color="#cbd5e1", line_width=1)
    fig_scatter.add_vline(x=0.0, line_dash="dash", line_color="#ef4444", line_width=2)
    
    x_min, x_max = filtered_summary['2020년_코로나_변동률(%)'].min(), filtered_summary['2020년_코로나_변동률(%)'].max()
    y_min, y_max = filtered_summary['10개년_평균_창업수(규모)'].min(), filtered_summary['10개년_평균_창업수(규모)'].max()
    
    x_pad = (x_max - x_min) * 0.1 if (x_max - x_min) != 0 else 10
    y_pad = (y_max - y_min) * 0.1 if (y_max - y_min) != 0 else 100
    
    fig_scatter.update_layout(
        dragmode='pan',
        xaxis=dict(
            title="2020년 창업 변동률 (기준: 0%)", 
            showgrid=True, 
            gridcolor="#e2e8f0",
            range=[x_min - x_pad, x_max + x_pad],
            fixedrange=False
        ),
        yaxis=dict(
            title="10개년 평균 창업 수 (규모)", 
            showgrid=True, 
            gridcolor="#e2e8f0",
            range=[y_min - y_pad, y_max + y_pad],
            fixedrange=False
        )
    )
    
    st.plotly_chart(fig_scatter, width='stretch', config={'displayModeBar': False, 'scrollZoom': True})
else:
    st.warning("🚨 선택하신 조건에 만족하는 업종이 없습니다. 필터 범위를 조절해보세요!")

st.markdown("---")

# 6. 메인 시각화 2: 영역 차트
st.markdown("### 📈 선택한 업종들의 10개년 창업 수 누적 변화 추이")
st.caption("선택된 세부 업종들이 지난 10년 동안 전체 시장에서 차지해 온 누적 크기를 비교합니다.")

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
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    val_max = filtered_raw.groupby('연度')['창업기업수'].sum().max() if '연度' in filtered_raw.columns else filtered_raw.groupby('연도')['창업기업수'].sum().max()
    
    fig_area.update_layout(
        dragmode='pan',
        xaxis=dict(
            title="연도 추이", 
            tickmode='linear', 
            showgrid=True, 
            gridcolor="#e2e8f0"
        ),
        yaxis=dict(
            title="누적 창업 기업 수", 
            showgrid=True, 
            gridcolor="#e2e8f0",
            range=[0, val_max * 1.05]
        )
    )
    st.plotly_chart(fig_area, width='stretch', config={'displayModeBar': False, 'scrollZoom': True})
else:
    st.info("💡 상단 매트릭스 지도에 표시된 업종이 없으면 누적 차트도 나타나지 않습니다.")

st.markdown("---")
st.caption("Data Source: 업종별 창업기업수 통계 (2016-2025) | Page 3")
