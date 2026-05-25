import math

import streamlit as st


APP_TITLE = "儿童SRNS患儿CNI耐药风险预测工具"
APP_SUBTITLE = "基于Logistic回归模型的CNI耐药早期预测"
CUTOFF = 0.18


def calculate_probability(gene: int, crp: float, tg: float, u_rbc: float) -> tuple[float, float]:
    """Return logit and predicted probability for CNI resistance."""
    logit = -2.914 + 3.528 * gene + 0.151 * crp - 0.194 * tg + 0.001 * u_rbc
    probability = 1 / (1 + math.exp(-logit))
    return logit, probability


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f6f9fc;
    }
    .block-container {
        max-width: 980px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .title {
        color: #0b5cab;
        font-size: clamp(1.45rem, 4vw, 2.05rem);
        font-weight: 750;
        margin-bottom: 0.25rem;
        line-height: 1.35;
        white-space: normal;
        overflow-wrap: anywhere;
        word-break: break-word;
    }
    .subtitle {
        color: #3d5f7f;
        font-size: 1.08rem;
        margin-bottom: 1.35rem;
    }
    .section-card {
        background: #ffffff;
        border: 1px solid #d9e6f2;
        border-radius: 8px;
        padding: 1.2rem 1.35rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(11, 92, 171, 0.06);
    }
    .section-title {
        color: #164f7f;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }
    .result-high {
        border-left: 6px solid #c62828;
        background: #fff5f5;
        padding: 1rem 1.1rem;
        border-radius: 8px;
    }
    .result-low {
        border-left: 6px solid #1b7f42;
        background: #f3fbf6;
        padding: 1rem 1.1rem;
        border-radius: 8px;
    }
    .probability {
        font-size: 2rem;
        font-weight: 800;
        color: #0b5cab;
        margin-bottom: 0.2rem;
    }
    .risk-label {
        font-size: 1.28rem;
        font-weight: 750;
        margin-bottom: 0;
    }
    .note {
        color: #516579;
        font-size: 0.95rem;
        line-height: 1.75;
    }
    .disclaimer {
        color: #6c757d;
        font-size: 0.9rem;
        border-top: 1px solid #d9e6f2;
        margin-top: 1rem;
        padding-top: 1rem;
        line-height: 1.7;
    }
