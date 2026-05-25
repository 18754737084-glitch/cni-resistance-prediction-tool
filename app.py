import streamlit as st
import math

st.set_page_config(
    page_title="儿童SRNS患儿CNI耐药风险预测工具",
    page_icon="🧬",
    layout="centered"
)

st.title("儿童SRNS患儿CNI耐药风险预测工具")
st.subheader("基于Logistic回归模型的CNI耐药早期预测")

st.markdown("""
本工具基于单基因变异、C反应蛋白、甘油三酯和尿红细胞计数构建，
用于辅助评估儿童激素耐药型肾病综合征患儿发生CNI耐药的风险。
""")

st.divider()

gene_option = st.selectbox(
    "单基因变异结果",
    options=["阴性", "阳性"]
)

gene = 1 if gene_option == "阳性" else 0

crp = st.number_input(
    "C反应蛋白 CRP（mg/L）",
    min_value=0.0,
    value=8.0,
    step=0.1
)

tg = st.number_input(
    "甘油三酯 TG（mmol/L）",
    min_value=0.0,
    value=3.0,
    step=0.1
)

u_rbc = st.number_input(
    "尿红细胞计数 U-RBC（个/μL）",
    min_value=0.0,
    value=100.0,
    step=1.0
)

if st.button("开始预测"):
    logit_p = -2.914 + 3.528 * gene + 0.151 * crp - 0.194 * tg + 0.001 * u_rbc
    probability = 1 / (1 + math.exp(-logit_p))

    st.divider()
    st.subheader("预测结果")

    st.metric(
        label="CNI耐药预测概率",
        value=f"{probability * 100:.2f}%"
    )

    if probability >= 0.18:
        st.error("风险判断：CNI耐药高风险")
        st.markdown("建议结合患儿临床表现、基因检测、病理结果及治疗反应，进一步评估是否需要优化免疫抑制治疗方案。")
    else:
        st.success("风险判断：CNI耐药低风险")
        st.markdown("提示患儿发生CNI耐药的预测风险较低，但仍需结合临床随访动态判断。")

st.divider()

st.markdown("""
### 模型信息

- 模型类型：多因素 Logistic 回归预测模型
- 纳入变量：单基因变异、CRP、TG、U-RBC
- AUC：0.85
- 灵敏度：0.72
- 特异度：0.91
- 最佳截断值：0.18

### 免责声明

本工具仅用于科研和临床辅助参考，不能替代医生的临床判断。
正式临床应用前，仍需进行多中心外部验证和前瞻性验证。
""")
