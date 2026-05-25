import math

import streamlit as st


APP_TITLE = "\u513f\u7ae5SRNS\u60a3\u513fCNI\u8010\u836f\u98ce\u9669\u9884\u6d4b\u5de5\u5177"
APP_SUBTITLE = "\u57fa\u4e8eLogistic\u56de\u5f52\u6a21\u578b\u7684CNI\u8010\u836f\u65e9\u671f\u9884\u6d4b"
CUTOFF = 0.18

LABEL_INPUT = "\u9884\u6d4b\u53d8\u91cf\u8f93\u5165"
LABEL_GENE = "\u5355\u57fa\u56e0\u53d8\u5f02"
LABEL_CRP = "C\u53cd\u5e94\u86cb\u767d CRP\uff08mg/L\uff09"
LABEL_TG = "\u7518\u6cb9\u4e09\u916f TG\uff08mmol/L\uff09"
LABEL_URBC = "\u5c3f\u7ea2\u7ec6\u80de\u8ba1\u6570 U-RBC\uff08\u4e2a/\u03bcL\uff09"
LABEL_RESULT = "\u9884\u6d4b\u7ed3\u679c"
LABEL_MODEL = "\u6a21\u578b\u8bf4\u660e"
LABEL_CUTOFF = "\u98ce\u9669\u622a\u65ad\u503c"

GENE_NEGATIVE = "\u9634\u6027 = 0"
GENE_POSITIVE = "\u9633\u6027 = 1"
HELP_GENE = "\u8bf7\u9009\u62e9\u60a3\u513f\u662f\u5426\u5b58\u5728\u5355\u57fa\u56e0\u53d8\u5f02\u3002"
HIGH_RISK = "CNI\u8010\u836f\u9ad8\u98ce\u9669"
LOW_RISK = "CNI\u8010\u836f\u4f4e\u98ce\u9669"

MODEL_DESCRIPTION = (
    "\u672c\u5de5\u5177\u57fa\u4e8e\u5355\u57fa\u56e0\u53d8\u5f02\u3001CRP\u3001TG\u3001U-RBC\u56db\u4e2a\u53d8\u91cf\u6784\u5efa\u3002<br>"
    "Logistic\u56de\u5f52\u516c\u5f0f\uff1alogit(P) = -2.914 + 3.528 \u00d7 gene + 0.151 \u00d7 CRP - 0.194 \u00d7 TG + 0.001 \u00d7 U-RBC\u3002<br>"
    "\u6a21\u578b\u6027\u80fd\uff1aAUC=0.85\uff0c\u7075\u654f\u5ea6=0.72\uff0c\u7279\u5f02\u5ea6=0.91\uff0c\u6700\u4f73\u622a\u65ad\u503c=0.18\u3002"
)
DISCLAIMER = (
    "\u514d\u8d23\u58f0\u660e\uff1a\u672c\u5de5\u5177\u4ec5\u7528\u4e8e\u79d1\u7814\u548c\u4e34\u5e8a\u8f85\u52a9\u53c2\u8003\uff0c"
    "\u4e0d\u80fd\u66ff\u4ee3\u533b\u751f\u7684\u4e34\u5e8a\u5224\u65ad\u3002"
    "\u6b63\u5f0f\u5e94\u7528\u524d\u9700\u8fdb\u884c\u5916\u90e8\u9a8c\u8bc1\u3002"
)


def calculate_probability(gene: int, crp: float, tg: float, u_rbc: float) -> tuple[float, float]:
    logit = -2.914 + 3.528 * gene + 0.151 * crp - 0.194 * tg + 0.001 * u_rbc
    probability = 1 / (1 + math.exp(-logit))
    return logit, probability


st.set_page_config(
    page_title=APP_TITLE,
    page_icon=":hospital:",
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
        max-width: 620px;
        padding-top: 4rem;
        padding-bottom: 2rem;
    }
    h3 {
        color: #0b5cab;
        font-size: 24px;
        font-weight: 750;
        line-height: 1.6;
        margin-top: 0;
        margin-bottom: 8px;
        max-width: 100%;
        white-space: normal;
        overflow-wrap: break-word;
    }
    .subtitle {
        color: #3d5f7f;
        font-size: 16px;
        margin-bottom: 28px;
        line-height: 1.5;
    }
    .section-title {
        color: #164f7f;
        font-size: 20px;
        font-weight: 700;
        margin-top: 22px;
        margin-bottom: 12px;
    }
    .result-high {
        border-left: 6px solid #c62828;
        background: #fff5f5;
        padding: 18px 22px;
        border-radius: 8px;
    }
    .result-low {
        border-left: 6px solid #1b7f42;
        background: #f3fbf6;
        padding: 18px 22px;
        border-radius: 8px;
    }
    .probability {
        font-size: 34px;
        font-weight: 800;
        color: #0b5cab;
        margin-bottom: 6px;
    }
    .risk-label {
        font-size: 18px;
        font-weight: 750;
        margin-bottom: 0;
    }
    .section-card {
        background: #ffffff;
        border: 1px solid #d9e6f2;
        border-radius: 8px;
        padding: 18px 22px;
        margin-bottom: 18px;
        box-shadow: 0 2px 10px rgba(11, 92, 171, 0.06);
    }
    .note {
        color: #516579;
        font-size: 15px;
        line-height: 1.8;
    }
    .disclaimer {
        color: #6c757d;
        font-size: 14px;
        border-top: 1px solid #d9e6f2;
        margin-top: 24px;
        padding-top: 16px;
        line-height: 1.7;
    }
    div[data-testid="stSelectbox"], div[data-testid="stNumberInput"] {
        margin-bottom: 12px;
    }
    div[data-testid="stMetricValue"] {
        color: #0b5cab;
        font-size: 34px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(f"### {APP_TITLE}")
st.markdown(f'<div class="subtitle">{APP_SUBTITLE}</div>', unsafe_allow_html=True)

st.markdown(f'<div class="section-title">{LABEL_INPUT}</div>', unsafe_allow_html=True)

gene_label = st.selectbox(
    LABEL_GENE,
    options=[GENE_NEGATIVE, GENE_POSITIVE],
    help=HELP_GENE,
)
crp = st.number_input(
    LABEL_CRP,
    min_value=0.0,
    value=5.0,
    step=0.1,
    format="%.2f",
)
tg = st.number_input(
    LABEL_TG,
    min_value=0.0,
    value=1.50,
    step=0.01,
    format="%.2f",
)
u_rbc = st.number_input(
    LABEL_URBC,
    min_value=0.0,
    value=20.0,
    step=1.0,
    format="%.2f",
)

gene = 1 if gene_label == GENE_POSITIVE else 0
logit, probability = calculate_probability(gene, crp, tg, u_rbc)
probability_percent = probability * 100
is_high_risk = probability >= CUTOFF
risk_text = HIGH_RISK if is_high_risk else LOW_RISK
risk_class = "result-high" if is_high_risk else "result-low"

st.markdown(f'<div class="section-title">{LABEL_RESULT}</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="{risk_class}">
        <div class="probability">{probability_percent:.2f}%</div>
        <p class="risk-label">{risk_text}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_col1, metric_col2 = st.columns(2)
with metric_col1:
    st.metric("Logit(P)", f"{logit:.3f}")
with metric_col2:
    st.metric(LABEL_CUTOFF, f"{CUTOFF:.2f}")

st.markdown(f'<div class="section-title">{LABEL_MODEL}</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="section-card note">
    {MODEL_DESCRIPTION}
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="disclaimer">
    {DISCLAIMER}
    </div>
    """,
    unsafe_allow_html=True,
)
