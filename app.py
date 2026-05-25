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
    div[data-testid="stMetricValue"] {
        color: #0b5cab;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(f'<div class="title">{APP_TITLE_HTML}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{APP_SUBTITLE}</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">预测变量输入</div>', unsafe_allow_html=True)

gene_label = st.selectbox(
    "单基因变异",
    options=["阴性 = 0", "阳性 = 1"],
    help="请选择患儿是否存在单基因变异。",
)
crp = st.number_input(
    "C反应蛋白 CRP（mg/L）",
    min_value=0.0,
    value=5.0,
    step=0.1,
    format="%.2f",
)
tg = st.number_input(
    "甘油三酯 TG（mmol/L）",
    min_value=0.0,
    value=1.50,
    step=0.01,
    format="%.2f",
)
u_rbc = st.number_input(
    "尿红细胞计数 U-RBC（个/μL）",
    min_value=0.0,
    value=20.0,
    step=1.0,
    format="%.2f",
)

gene = 1 if gene_label.startswith("阳性") else 0
logit, probability = calculate_probability(gene, crp, tg, u_rbc)
probability_percent = probability * 100
is_high_risk = probability >= CUTOFF
risk_text = "CNI耐药高风险" if is_high_risk else "CNI耐药低风险"
risk_class = "result-high" if is_high_risk else "result-low"

st.markdown('<div class="section-title">预测结果</div>', unsafe_allow_html=True)
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
    st.metric("风险截断值", f"{CUTOFF:.2f}")

st.markdown('<div class="section-title">模型说明</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-card note">
    本工具基于单基因变异、CRP、TG、U-RBC四个变量构建。<br>
    Logistic回归公式：logit(P) = -2.914 + 3.528 × gene + 0.151 × CRP - 0.194 × TG + 0.001 × U-RBC。<br>
    模型性能：AUC=0.85，灵敏度=0.72，特异度=0.91，最佳截断值=0.18。
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="disclaimer">
    免责声明：本工具仅用于科研和临床辅助参考，不能替代医生的临床判断。正式应用前需进行外部验证。
    </div>
    """,
