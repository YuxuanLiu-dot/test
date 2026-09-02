"""
Power Tools Industry Monitor
=================================================================
Wind × Python × AI Summer Camp — Day 5 项目模板

这个应用只做一件事：把 Notebook 导出的 CSV 读进来，画在网页上。
所有的分析都已经在 Notebook 里做完了。

要改成你自己的项目，请搜索 "TODO" 并按提示修改。
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------- 页面配置
# TODO 1：把标题改成你自己的项目名
APP_TITLE = "Power Tools Industry Monitor"
APP_SUBTITLE = "从美国利率环境到电动工具龙头的股价表现"

st.set_page_config(page_title=APP_TITLE, page_icon="📊", layout="wide")

DATA_DIR = Path(__file__).parent / "data"


# ---------------------------------------------------------------- 读数据
@st.cache_data
def load_csv(filename, index_col, parse_dates=False):
    """读取 data/ 文件夹里的一个 CSV。找不到就返回 None。"""
    path = DATA_DIR / filename
    if not path.exists():
        return None
    return pd.read_csv(path, index_col=index_col, parse_dates=parse_dates)


#macro = load_csv("macro_monthly.csv", index_col="Date", parse_dates=True)
normalized = load_csv("market_normalized.csv", index_col="Date", parse_dates=True)
prices = load_csv("market_prices.csv", index_col="Date", parse_dates=True)
snapshot = load_csv("company_snapshot.csv", index_col="Security")
data_dict = load_csv("data_dictionary.csv", index_col=None)

if macro is None:
    st.error(
        "找不到 `data/macro_monthly.csv`。\n\n"
        "请先运行 Notebook 的 Part 8 导出数据，"
        "再把 `day5_output/` 里的 CSV 上传到本仓库的 `data/` 文件夹。"
    )
    st.stop()


# ---------------------------------------------------------------- 标题
st.title(APP_TITLE)
st.caption(APP_SUBTITLE)


# ---------------------------------------------------------------- 侧边栏
st.sidebar.header("筛选")

min_date = macro.index.min().date()
max_date = macro.index.max().date()

start_date, end_date = st.sidebar.select_slider(
    "时间范围",
    options=list(macro.index.date),
    value=(min_date, max_date),
)

st.sidebar.markdown("---")
# TODO 2：如果你的宏观指标不一样，这里的默认选项要改
available = [c for c in macro.columns]
chosen = st.sidebar.multiselect(
    "宏观指标",
    options=available,
    default=[c for c in ["US_10Y_Treasury", "US_30Y_Mortgage"] if c in available],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**数据来源**\n\n"
    "宏观数据：Demo \n\n"
    "股价与估值：Demo \n\n"
    "*本应用仅用于教学，不构成投资建议。*"
)

macro_view = macro.loc[str(start_date):str(end_date)]


# ---------------------------------------------------------------- 关键指标
st.subheader("当前状况")

cols = st.columns(4)
metric_specs = [
    ("US_10Y_Treasury", "10 年期国债收益率", "%"),
    ("US_30Y_Mortgage", "30 年期房贷利率", "%"),
    ("US_New_Home_Sales", "新屋销售", "千套"),
    ("Spread", "房贷利差", "pp"),
]
for col, (key, label, unit) in zip(cols, metric_specs):
    if key not in macro_view.columns:
        continue
    series = macro_view[key].dropna()
    if series.empty:
        continue
    latest = series.iloc[-1]
    change = latest - series.iloc[0]
    col.metric(label, f"{latest:,.2f} {unit}", f"{change:+.2f}")


# ---------------------------------------------------------------- 宏观
st.markdown("---")
st.subheader("1　宏观环境")

if chosen:
    st.line_chart(macro_view[chosen], height=320)
else:
    st.info("请在左侧至少选择一个宏观指标。")

# TODO 3：把下面这段换成你自己的观察
st.markdown(
    "**观察：** 房贷利率与国债收益率高度同步，两者之差在样本期内相对稳定，"
    "说明房贷利率的变化主要由长端利率驱动，而不是信用利差。"
)

if "US_30Y_Mortgage" in macro_view and "US_New_Home_Sales" in macro_view:
    left, right = st.columns([2, 1])
    with left:
        st.markdown("**房贷利率 vs 新屋销售**")
        scatter_df = macro_view[["US_30Y_Mortgage", "US_New_Home_Sales"]].dropna()
        st.scatter_chart(scatter_df, x="US_30Y_Mortgage", y="US_New_Home_Sales",
                         height=300)
    with right:
        st.markdown("**相关系数**")
        corr = macro_view[[c for c in macro.columns if c != "Spread"]].corr()
        st.dataframe(corr.round(2), width="stretch")
        st.caption("Correlation ≠ Causation")


# ---------------------------------------------------------------- 股价
if normalized is not None:
    st.markdown("---")
    st.subheader("2　股价表现（起点 = 100）")

    norm_view = normalized.loc[str(start_date):str(end_date)]
    if not norm_view.empty:
        norm_view = norm_view / norm_view.iloc[0] * 100
    st.line_chart(norm_view, height=320)

    # TODO 4：换成你自己的观察
    st.markdown(
        "**观察：** 两家公司在利率上行期同步回撤，说明它们共同暴露在"
        "同一个终端需求变量（美国房地产活动）之下。"
    )

    if prices is not None:
        with st.expander("日收益率与年化波动率"):
            returns = prices.loc[str(start_date):str(end_date)].pct_change().dropna()
            vol = (returns.std() * (252 ** 0.5) * 100).round(1)
            st.dataframe(
                pd.DataFrame({"年化波动率 (%)": vol}),
                width="stretch",
            )


# ---------------------------------------------------------------- 公司
if snapshot is not None:
    st.markdown("---")
    st.subheader("3　公司截面对比")

    left, right = st.columns([1, 1])
    numeric_cols = [c for c in snapshot.columns
                    if pd.api.types.is_numeric_dtype(snapshot[c])]
    with left:
        multiples = [c for c in numeric_cols if "Cap" not in c]
        if multiples:
            st.bar_chart(snapshot[multiples], height=300)
    with right:
        st.dataframe(snapshot, width="stretch")


# ---------------------------------------------------------------- Findings
st.markdown("---")
st.subheader("4　Findings")

# TODO 5：写 3–5 条你自己的发现。这是整个项目最重要的部分。
st.markdown(
    """
1. 30 年期房贷利率与 10 年期国债收益率高度相关，利差长期稳定在 2–3 个百分点。
2. 房贷利率与新屋销售呈负相关，与 Day 2 的行业逻辑一致。
3. 两家电动工具公司的股价在利率上行期同步承压。
4. *（把这一条换成你自己的发现）*
5. *（把这一条换成你自己的发现）*
"""
)


# ---------------------------------------------------------------- 数据字典
if data_dict is not None:
    with st.expander("数据字典 / Data Dictionary"):
        st.dataframe(data_dict, width="stretch", hide_index=True)

st.markdown("---")
st.caption(
    "Wind × Python × AI Summer Camp · Day 5 Project　|　"
    "宏观数据来源：FRED, Federal Reserve Bank of St. Louis　|　"
    "本应用仅用于教学演示，不构成投资建议。"
)
