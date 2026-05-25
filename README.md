# 儿童SRNS患儿CNI耐药风险预测工具

这是一个基于 Streamlit 构建的在线临床预测工具，用于根据 Logistic 回归模型早期预测儿童激素耐药型肾病综合征（SRNS）患儿发生钙调神经磷酸酶抑制剂（CNI）耐药的风险。

## 在线工具主题

- 页面标题：儿童SRNS患儿CNI耐药风险预测工具
- 页面副标题：基于Logistic回归模型的CNI耐药早期预测

## 输入变量

工具包含以下四个预测变量：

- 单基因变异：阴性=0，阳性=1
- C反应蛋白 CRP，单位 mg/L
- 甘油三酯 TG，单位 mmol/L
- 尿红细胞计数 U-RBC，单位 个/μL

## 模型公式

```text
logit(P) = -2.914 + 3.528 * gene + 0.151 * CRP - 0.194 * TG + 0.001 * U_RBC
P = 1 / (1 + exp(-logit(P)))
```

预测概率以百分比显示，并保留两位小数。

## 风险判断

使用最佳截断值 0.18 进行风险分层：

- P >= 0.18：CNI耐药高风险
- P < 0.18：CNI耐药低风险

## 模型性能

- AUC = 0.85
- 灵敏度 = 0.72
- 特异度 = 0.91
- 最佳截断值 = 0.18

## 本地运行

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 启动应用：

```bash
streamlit run app.py
```

## Streamlit Community Cloud 部署

将本项目上传至 GitHub，并在 Streamlit Community Cloud 中选择该仓库。部署入口文件设置为：

```text
app.py
```

依赖文件为：

```text
requirements.txt
```

## 免责声明

本工具仅用于科研和临床辅助参考，不能替代医生的临床判断。正式应用前需进行外部验证。
