# -*- coding: utf-8 -*-
"""
数据岗 JD 技能-薪资关联分析（主项目核心模块）
============================================
回答三个问题：
  1. 数据岗 JD 里什么技能出现频率最高？（技能需求地图）
  2. 哪些技能与更高薪资相关？（技能溢价分析）
  3. 不同城市的薪资水平差多少？（城市对比）

知识点：
  - 数据清洗：解析 '15-28K·14薪' / '220-250元/天' 两类薪资格式 → 统一月薪口径
  - 词频统计：skills 列表打平 + value_counts
  - 关联分析：分组均值对比（含某技能 vs 不含）→ 溢价 = 差值/整体均值
  - 数据口径意识：实习日薪与正式月薪口径不同，必须分开统计

数据源：BOSS 直聘公开岗位数据（resume_pipeline 采集，原始数据不入库）
"""
import json
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

DATA = r"D:/Documents/Tools/resume_pipeline/data/jobs/screened_20260927.json"
OUT = r"C:/Users/12923/Desktop/job-market-analysis/output"


def load_and_clean():
    df = pd.DataFrame(json.load(open(DATA, encoding="utf-8")))
    # 去重（同 job_id 保留最新）
    df = df.drop_duplicates(subset="job_id", keep="last")
    return df


def parse_salary(s):
    """解析 BOSS 薪资格式 → (月薪中位数K, 口径)
    月薪：'15-28K·14薪' → 中位 (15+28)/2 = 21.5K
    日薪：'220-250元/天' → 中位 × 22 个工作日 ≈ 月薪
    """
    if not isinstance(s, str):
        return None, None
    m = re.match(r"(\d+)-(\d+)K", s)
    if m:
        return (int(m.group(1)) + int(m.group(2))) / 2, "month"
    m = re.match(r"(\d+)-(\d+)元/天", s)
    if m:
        daily = (int(m.group(1)) + int(m.group(2))) / 2
        return round(daily * 22 / 1000, 1), "day"
    return None, None


def skill_salary_analysis(df):
    """技能-薪资关联：每个技能出现频次 + 平均薪资溢价"""
    # 薪资解析
    parsed = df["salary"].apply(parse_salary)
    df["salary_mid_k"] = parsed.apply(lambda x: x[0])
    df["salary_type"] = parsed.apply(lambda x: x[1])
    print("薪资格式分布:", df["salary_type"].value_counts().to_dict())
    print("月薪岗位解析成功率:",
          (df["salary_mid_k"].notna()).mean().round(3))

    month_df = df[df["salary_type"] == "month"].copy()
    print(f"\n正式岗（月薪口径）: {len(month_df)} 个, "
          f"平均月薪 {month_df['salary_mid_k'].mean():.1f}K")

    # 技能词频
    all_skills = month_df["skills"].explode().dropna()
    skill_freq = all_skills.value_counts()
    print(f"\n技能种类 {skill_freq.nunique()} 个, 出现总次数 {len(all_skills)}")
    print("Top 15 高频技能:")
    print(skill_freq.head(15).to_string())

    # 技能-薪资溢价（出现频次 >= 20 的技能才有统计意义）
    base = month_df["salary_mid_k"].mean()
    rows = []
    for skill in skill_freq[skill_freq >= 20].index:
        has = month_df[month_df["skills"].apply(
            lambda s, sk=skill: isinstance(s, list) and sk in s)]
        no = month_df[month_df["skills"].apply(
            lambda s, sk=skill: not (isinstance(s, list) and sk in s))]
        rows.append({
            "技能": skill,
            "出现次数": len(has),
            "含技能平均月薪K": round(has["salary_mid_k"].mean(), 2),
            "不含平均月薪K": round(no["salary_mid_k"].mean(), 2),
            "溢价%": round((has["salary_mid_k"].mean() / base - 1) * 100, 1),
        })
    premium = pd.DataFrame(rows).sort_values("溢价%", ascending=False)
    print(f"\n技能薪资溢价排行（全体均值 {base:.1f}K，频次≥20）：")
    print(premium.head(15).to_string(index=False))

    # 城市-薪资
    city = month_df.groupby("city").agg(
        岗位数=("job_id", "count"),
        平均月薪K=("salary_mid_k", "mean"),
    ).sort_values("平均月薪K", ascending=False)
    print("\n城市薪资对比（正式岗）：")
    print(city.round(1).to_string())

    # 学历要求
    edu = month_df["education"].value_counts()
    print("\n学历要求分布:")
    print(edu.head(6).to_string())

    return month_df, skill_freq, premium, city


def make_charts(month_df, skill_freq, premium, city):
    # 图 1：Top 15 技能词频
    fig, ax = plt.subplots(figsize=(10, 5))
    s = skill_freq.head(15).sort_values()
    ax.barh(s.index, s.values, color="#2B579A")
    ax.set_title("数据岗 JD Top 15 高频技能")
    ax.set_xlabel("出现次数")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"{OUT}/01_skill_freq.png", dpi=130)
    plt.close(fig)

    # 图 2：技能溢价 Top 10 / Bottom 5
    fig, ax = plt.subplots(figsize=(10, 6))
    show = pd.concat([premium.head(10), premium.tail(5)])
    colors = ["#C00000" if v > 0 else "#2B579A" for v in show["溢价%"]]
    ax.barh(show["技能"], show["溢价%"], color=colors)
    ax.axvline(0, color="gray", lw=0.8)
    ax.set_title("技能薪资溢价（相对全体均值，%）")
    ax.set_xlabel("溢价 %")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"{OUT}/02_skill_premium.png", dpi=130)
    plt.close(fig)

    # 图 3：城市平均薪资
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(city.index, city["平均月薪K"], color="#2B579A")
    for i, v in enumerate(city["平均月薪K"]):
        ax.text(i, v + 0.3, f"{v:.1f}K", ha="center")
    ax.set_title("各城市数据岗平均月薪（正式岗）")
    ax.set_ylabel("平均月薪（K）")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"{OUT}/03_city_salary.png", dpi=130)
    plt.close(fig)
    print("\n✅ 3 张图表已保存到 output/")


if __name__ == "__main__":
    df = load_and_clean()
    print(f"清洗后样本: {len(df)} 条")
    month_df, skill_freq, premium, city = skill_salary_analysis(df)
    make_charts(month_df, skill_freq, premium, city)
