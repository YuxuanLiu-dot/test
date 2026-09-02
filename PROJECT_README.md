# Power Tools Industry Monitor

> **TODO：把这一行换成你自己的一句话简介。**
> 例如：一个追踪美国利率环境如何传导到电动工具行业需求与股价的交互式数据应用。

🔗 **在线应用：** <!-- TODO：部署完成后把网址贴在这里 -->
`https://你的用户名-项目名.streamlit.app`

---

## 研究问题

> **TODO：用一两句话说清楚你想回答什么问题。**

美国长端利率的变化，如何通过抵押贷款利率传导到房地产活动，
并最终影响电动工具行业两家龙头公司的股价表现？

传导链条：

```
美国 10 年期国债收益率
        ↓
30 年期固定抵押贷款利率
        ↓
新屋销售
        ↓
房地产活动
        ↓
电动工具需求
        ↓
创科实业 0669.HK / 泉峰控股 2285.HK
```

---

## 数据

| 数据 | 说明 | 频率 | 来源 |
|---|---|---|---|
| `DGS10` | 美国 10 年期国债收益率 | 日 | FRED（美联储理事会） |
| `MORTGAGE30US` | 30 年期固定抵押贷款利率 | 周 | FRED（Freddie Mac） |
| `HSN1F` | 新建独栋住宅销售，季调年化 | 月 | FRED（美国人口普查局，公共领域） |
| `CPIAUCSL` | 消费者价格指数 | 月 | FRED（美国劳工统计局） |
| 股价 / 估值 | 两家公司的收盘价与估值倍数 | 日 / 快照 | 课堂数据 |

每一列的完整定义见 [`data/data_dictionary.csv`](data/data_dictionary.csv)。

**引用格式：**
> Federal Reserve Bank of St. Louis, FRED Economic Data,
> https://fred.stlouisfed.org

---

## 分析方法

1. **取数** — 从 FRED 下载 CSV，读入 pandas
2. **对齐与变频** — 四个指标频率不同，统一 `resample()` 到月度
   - 利率用 `mean()`（一个月的平均水平）
   - 销售与 CPI 用 `last()`（月末值）
3. **构造衍生指标** — 抵押贷款利差 = 房贷利率 − 国债收益率
4. **归一化股价** — 每条价格序列除以期初值 × 100，使不同价位的股票可比
5. **描述性分析** — 相关系数矩阵、散点图、年化波动率

分析全过程见 [`notebook/analysis.ipynb`](notebook/analysis.ipynb)。

---

## Findings

> **TODO：写 3–5 条你自己的发现。这是整个项目最重要的部分。**
> 每一条都要是一个可以被数据支持的**结论**，而不是对图表的描述。
> ❌「我画了一张利率的折线图」
> ✅「房贷利差在样本期内稳定在 2–3 个百分点，说明房贷利率的变化主要由长端利率驱动」

1. 30 年期房贷利率与 10 年期国债收益率高度相关，两者利差长期稳定在 2–3 个百分点。
2. 房贷利率与新屋销售呈负相关，与利率敏感型需求的行业逻辑一致。
3. 两家电动工具公司股价在利率上行期同步承压，说明二者共同暴露于同一个终端需求变量。
4. *（换成你自己的发现）*
5. *（换成你自己的发现）*

**局限性：** 相关不等于因果。本文只做描述性分析，没有控制其他变量，
也没有处理传导的时滞问题。

---

## 应用截图

> **TODO：部署完成后截一张图，拖进 GitHub 的编辑器里，把生成的链接贴在这里。**

<!-- ![screenshot](docs/screenshot.png) -->

---

## 仓库结构

```
├── streamlit_app.py            交互式应用
├── requirements.txt            依赖清单
├── data/
│   ├── macro_monthly.csv       宏观月度数据
│   ├── market_prices.csv       股价收盘价
│   ├── market_normalized.csv   归一化股价（起点 = 100）
│   ├── company_snapshot.csv    公司估值截面
│   ├── correlation.csv         相关系数矩阵
│   └── data_dictionary.csv     数据字典
└── notebook/
    └── analysis.ipynb          完整分析过程
```

---

## 本地运行

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 声明

本项目为 **Wind × Python × AI 暑期训练营** 的教学作业，
仅用于学习与演示，**不构成任何投资建议**。

宏观数据来自 FRED 公开数据库，遵循其使用条款。
