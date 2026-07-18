import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy.special import erf

st.set_page_config(
    page_title="오차함수 열확산 시뮬레이션",
    page_icon="🌡️",
    layout="wide",
)

st.title("오차함수를 이용한 열확산 시뮬레이션")
st.caption(
    "반무한 고체의 1차원 열확산 해를 계산하고, "
    "이를 원형 단면으로 나타낸 교육용 단순화 모델입니다."
)

st.latex(
    r"T(x,t)=T_s+(T_i-T_s)\operatorname{erf}"
    r"\left(\frac{x}{2\sqrt{\alpha t}}\right)"
)

with st.sidebar:
    st.header("조건 설정")
    Ti = st.number_input("초기 온도 Ti (℃)", value=60.0, step=1.0)
    Ts = st.number_input("표면 온도 Ts (℃)", value=20.0, step=1.0)
    alpha = st.number_input(
        "열확산계수 α (m²/s)",
        min_value=0.000001,
        max_value=0.01,
        value=0.0001,
        step=0.00001,
        format="%.6f",
    )
    t = st.slider("경과 시간 t (s)", 1, 100, 1, 1)
    max_depth = st.slider(
        "계산할 최대 깊이 (m)",
        min_value=0.01,
        max_value=0.10,
        value=0.04,
        step=0.005,
        format="%.3f",
    )
    radius = st.slider(
        "원형 단면 반지름 (m)",
        min_value=0.01,
        max_value=0.10,
        value=0.04,
        step=0.005,
        format="%.3f",
    )

denominator = 2 * np.sqrt(alpha * t)

col1, col2, col3 = st.columns(3)
col1.metric("초기 온도", f"{Ti:.1f} ℃")
col2.metric("표면 온도", f"{Ts:.1f} ℃")
col3.metric("2√(αt)", f"{denominator:.5f} m")

st.subheader("1. 거리별 온도 분포")

x = np.linspace(0, max_depth, 400)
eta = x / denominator
temperature = Ts + (Ti - Ts) * erf(eta)

line_fig = go.Figure()
line_fig.add_trace(
    go.Scatter(
        x=x,
        y=temperature,
        mode="lines",
        name="온도",
    )
)
line_fig.update_layout(
    title="거리별 온도 분포",
    xaxis_title="표면으로부터의 거리 x (m)",
    yaxis_title="온도 T (℃)",
    hovermode="x unified",
)
st.plotly_chart(line_fig, use_container_width=True)

sample_x = np.linspace(0, max_depth, 9)
sample_eta = sample_x / denominator
sample_erf = erf(sample_eta)
sample_temp = Ts + (Ti - Ts) * sample_erf

table = pd.DataFrame(
    {
        "거리 x (m)": np.round(sample_x, 5),
        "x / 2√(αt)": np.round(sample_eta, 4),
        "erf 값": np.round(sample_erf, 4),
        "온도 T (℃)": np.round(sample_temp, 2),
    }
)

st.dataframe(table, use_container_width=True, hide_index=True)
st.download_button(
    "계산표 CSV 내려받기",
    data=table.to_csv(index=False).encode("utf-8-sig"),
    file_name="temperature_distribution.csv",
    mime="text/csv",
)

st.subheader("2. 원형 단면 온도 히트맵")

grid_n = 260
axis = np.linspace(-radius, radius, grid_n)
X, Y = np.meshgrid(axis, axis)
r = np.sqrt(X**2 + Y**2)

depth = radius - r
inside = r <= radius

circular_temperature = np.full_like(r, np.nan, dtype=float)
valid_depth = np.maximum(depth[inside], 0)
circular_temperature[inside] = (
    Ts + (Ti - Ts) * erf(valid_depth / denominator)
)

heatmap_fig = go.Figure(
    data=go.Heatmap(
        x=axis,
        y=axis,
        z=circular_temperature,
        colorbar={"title": "온도 (℃)"},
        hovertemplate=(
            "x=%{x:.4f} m<br>"
            "y=%{y:.4f} m<br>"
            "온도=%{z:.2f} ℃<extra></extra>"
        ),
    )
)
heatmap_fig.update_layout(
    title="단순화된 원형 단면 온도 분포",
    xaxis_title="x 방향 위치 (m)",
    yaxis_title="y 방향 위치 (m)",
    yaxis={"scaleanchor": "x", "scaleratio": 1},
)
st.plotly_chart(heatmap_fig, use_container_width=True)

st.info(
    "원형 히트맵은 1차원 해를 원형 단면에 적용해 만든 시각화이다. "
    "실제 원통형 배터리는 내부 발열과 방향별 물성 등을 포함하므로 더 복잡하다."
)

st.subheader("3. 특정 위치 온도 계산")

point_x = st.number_input(
    "표면으로부터의 거리 x (m)",
    min_value=0.0,
    max_value=float(max_depth),
    value=min(0.01, float(max_depth)),
    step=0.001,
    format="%.3f",
)

point_eta = point_x / denominator
point_erf = erf(point_eta)
point_temp = Ts + (Ti - Ts) * point_erf

st.write(f"x / 2√(αt) = **{point_eta:.4f}**")
st.write(f"erf 값 = **{point_erf:.4f}**")
st.success(f"계산된 온도: {point_temp:.2f} ℃")

with st.expander("모델의 가정과 해석"):
    st.write(
        """
        이 시뮬레이션은 표면 온도가 순간적으로 일정하게 바뀐
        반무한 고체의 1차원 열확산을 가정한다.
        x=0은 물체의 표면이고, x가 증가할수록 물체 내부를 뜻한다.
        냉각 상황에서는 표면 온도 Ts가 초기 온도 Ti보다 낮기 때문에
        표면에서 멀어질수록 온도가 초기 온도에 가까워진다.
        """
    )
